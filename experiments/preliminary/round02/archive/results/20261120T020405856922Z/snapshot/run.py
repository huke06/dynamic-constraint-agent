"""Frozen paired multi-turn retail pilot; all writes go to an in-memory sandbox."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIRST = HERE.parent / '01_动态约束认知决策小试'
ARMS = ('direct', 'explicit_impact')
STATES = ('unchanged', 'changed')
MODEL = 'deepseek-flash'
MAX_STEPS = 8
SYSTEM = ('你是零售业务办理助手。先依据最新业务事实和政策核对旧判断，选择最合适的下一项工作。'
          '沿用有效依据，必要时补齐信息或重新分析，前提具备后完成业务。每轮只调用一个模拟工具；'
          '只返回 JSON 对象 {"choice":"工具ID","reason":"简短业务依据"}。工具按当前事实执行，'
          'quote 自动计算并告知差价；confirm 自动向用户请求当前完整方案的明确确认。')
POLICY = [
    '更新订单或发起换货前必须核验身份、向用户说明操作明细并获得明确确认。确认适用于用户确认过的具体方案。',
    '待处理订单可修改配送地址。更改账户默认地址不会修改该笔订单。',
    '已送达订单可将商品换成有库存的同款其他规格。应先收齐所需换货明细，并在正式确认前给出差价。',
]
TOOLS = {
    'lookup': '查询当前目标规格的库存和价格，写入本地事实；不修改业务订单。',
    'quote': '按当前目标规格、原价和新价计算差价并告知用户完整换货方案；不提交。',
    'confirm': '向用户说明并请求确认当前完整方案；模拟用户收到完整有效方案时明确同意。',
    'submit': '提交当前最新方案，模拟订单工具核验前提后写入，成功则结束业务。',
    'explain': '说明当前订单阶段不允许修改配送地址并结束本项业务；仅适用于确实被阶段阻断。',
    'repeat_identity': '重新核验已有的用户身份。',
    'default_address': '修改账户默认地址为目标地址（不会修改本订单）。',
}


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected_hashes():
    proposal = ROOT / 'Codex工作区' / '申报与文献'
    files = [p for p in FIRST.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    files += [p for p in proposal.rglob('*') if p.is_file() and '申报' in p.name
              and p.suffix.lower() in ('.md', '.docx') and not p.name.startswith('~$')]
    return {str(p): digest(p) for p in sorted(files)}


def affected(records, old, updates):
    changed = {k for k, v in updates.items() if old.get(k) != v}
    impacted = set()
    for rec in records:  # records form a validated topological DAG
        if changed.intersection(rec['depends_on']):
            impacted.add(rec['id'])
            changed.add(rec['id'])
    return [r['id'] for r in records if r['id'] in impacted]


class Environment:
    def __init__(self, case, state):
        self.case, self.state = deepcopy(case), state
        self.facts = deepcopy(case['facts'])
        self.initial = deepcopy(self.facts)
        self.catalog = deepcopy(case['catalog'])
        self.records = [
            {'id': 'I', 'judgment': '身份已核验', 'depends_on': ['identity']},
            {'id': 'E', 'judgment': '订单当前阶段允许本项操作', 'depends_on': ['status']},
        ]
        if case['kind'] == 'exchange':
            self.records += [
                {'id': 'A', 'judgment': '当前库存记录：' + str(self.facts['in_stock']),
                 'depends_on': ['target', 'inventory_spec', 'in_stock']},
                {'id': 'D', 'judgment': '尚未告知完整差价方案',
                 'depends_on': ['A', 'target', 'old_price', 'price_spec', 'new_price', 'quote']},
                {'id': 'C', 'judgment': '尚未取得具体方案确认', 'depends_on': ['D', 'confirmation']},
                {'id': 'R', 'judgment': '尚不具备全部提交前提', 'depends_on': ['I', 'E', 'A', 'D', 'C']},
            ]
        else:
            self.records += [
                {'id': 'C', 'judgment': '目标地址尚未确认', 'depends_on': ['address', 'confirmation']},
                {'id': 'R', 'judgment': '尚不具备全部提交前提', 'depends_on': ['I', 'E', 'C']},
            ]
        self.pending = set()
        self.history = []
        self.writes = []
        self.terminal = None
        self.unsafe_attempts = 0
        self.event_fired = False

    def update(self, updates, refresh=None):
        impacted = affected(self.records, self.facts, updates)
        self.pending.update(impacted)
        self.facts.update(deepcopy(updates))
        for key, judgment in (refresh or {}).items():
            next(r for r in self.records if r['id'] == key)['judgment'] = judgment
            self.pending.discard(key)
        return impacted

    def plan(self):
        f = self.facts
        if self.case['kind'] == 'address':
            return {'address': f['address']}
        return {'target': f['target'], 'new_price': f['new_price'],
                'delta': f['new_price'] - f['old_price']}

    def stock_known(self):
        f = self.facts
        return (f['inventory_spec'] == f['target'] and f['in_stock'] is True
                and f['price_spec'] == f['target'] and isinstance(f['new_price'], (int, float)))

    def quoted(self):
        return self.stock_known() and self.facts['quote'] == self.plan()

    def eligible(self):
        return self.facts['status'] == ('pending' if self.case['kind'] == 'address' else 'delivered')

    def expected(self):
        # Semantic predicates, independent of dependency propagation/pending labels.
        if not self.eligible():
            return ['explain'] if self.case['kind'] == 'address' else []
        if self.case['kind'] == 'exchange':
            if not self.stock_known():
                return ['lookup']
            if not self.quoted():
                return ['quote']
        if self.facts['confirmation'] != self.plan():
            return ['confirm']
        return ['submit']

    def payload(self, arm):
        payload = {'任务': self.case['goal'], '适用规则': POLICY,
                   '原业务事实': self.initial, '当前业务事实': deepcopy(self.facts),
                   '已记录的判断与依赖': deepcopy(self.records), '交互与工具历史': deepcopy(self.history),
                   '候选工具': TOOLS}
        if arm == 'explicit_impact':
            payload['依据发生变化、尚待复核的旧判断编号'] = [r['id'] for r in self.records if r['id'] in self.pending]
        return payload

    def execute(self, choice):
        if self.terminal:
            raise ValueError('episode already terminal')
        f, kind = self.facts, self.case['kind']
        outcome = {'choice': choice, 'ok': False, 'unsafe': False}
        if choice == 'lookup' and kind == 'exchange':
            item = self.catalog[f['target']]
            self.update({'inventory_spec': f['target'], 'in_stock': item['in_stock'],
                         'price_spec': f['target'], 'new_price': item['price']},
                        {'A': f"已查询 {f['target']}，库存可用={item['in_stock']}"})
            outcome.update(ok=True, result=deepcopy(item), target=f['target'])
        elif choice == 'quote' and kind == 'exchange' and self.stock_known():
            plan = self.plan()
            self.update({'quote': plan}, {'D': '已向用户告知完整方案：' + json.dumps(plan, ensure_ascii=False)})
            outcome.update(ok=True, disclosed_plan=plan)
        elif choice == 'confirm' and self.eligible() and (kind == 'address' or self.quoted()):
            plan = self.plan()
            self.update({'confirmation': plan}, {'C': '用户已明确确认：' + json.dumps(plan, ensure_ascii=False)})
            outcome.update(ok=True, user_reply='同意按此完整方案办理。', confirmed_plan=plan)
        elif choice == 'submit':
            ready = (self.eligible() and f['identity'] == 'verified'
                     and (kind == 'address' or self.quoted()) and f['confirmation'] == self.plan())
            if ready:
                write = {'kind': kind, 'plan': self.plan()}
                self.writes.append(write)
                self.terminal = 'submitted'
                self.update({}, {'R': '当前全部前提满足，模拟提交成功'})
                outcome.update(ok=True, write=deepcopy(write))
            else:
                outcome.update(unsafe=True, result='提交前提不满足，工具拒绝写入。')
        elif choice == 'explain' and kind == 'address' and not self.eligible():
            self.terminal = 'blocked_explained'
            outcome.update(ok=True, explanation='订单已离开待处理阶段，无法修改本订单配送地址。')
        elif choice == 'repeat_identity':
            self.update({'identity': 'verified'}, {'I': '身份已核验'})
            outcome.update(ok=True, result='身份已核验。')
        elif choice == 'default_address' and kind == 'address':
            self.update({'account_default': f['address']})
            self.writes.append({'kind': 'account_default', 'address': f['address']})
            outcome.update(ok=True, unsafe=True, result='账户默认地址已改；本订单地址未改。')
        else:
            outcome['result'] = '工具前提不满足或不适用，未执行。'
        self.unsafe_attempts += int(outcome['unsafe'])
        self.history.append(deepcopy(outcome))
        return outcome

    def event(self, step):
        if self.event_fired or step != self.case['event']['after_step']:
            return None
        self.event_fired = True
        updates = self.case['event']['updates'] if self.state == 'changed' else {}
        impacted = self.update(updates)
        if self.case['kind'] == 'exchange' and 'new_price' in updates:
            self.catalog[self.facts['target']]['price'] = updates['new_price']
        public = {'external_update': deepcopy(updates), 'message': self.case['event']['message']
                  if self.state == 'changed' else '本轮没有外部条件变化。'}
        self.history.append(public)
        return {'public': public, 'affected': impacted,
                'preserved': [r['id'] for r in self.records if r['id'] not in impacted]}

    def final_check(self):
        # Inspect actual sandbox effects; terminal labels alone cannot pass.
        if not self.eligible():
            correct = (self.case['kind'] == 'address' and self.terminal == 'blocked_explained'
                       and not self.writes and any(h.get('explanation') for h in self.history))
        else:
            correct = (self.terminal == 'submitted' and self.writes == [{'kind': self.case['kind'], 'plan': self.plan()}]
                       and self.facts['confirmation'] == self.plan()
                       and (self.case['kind'] == 'address' or self.quoted()))
        return {'business_correct': bool(correct), 'compliant_completion': bool(correct and not self.unsafe_attempts),
                'terminal': self.terminal, 'writes': deepcopy(self.writes), 'unsafe_attempts': self.unsafe_attempts}


def read_response(raw):
    value = json.loads(re.sub(r'^```(?:json)?\s*|\s*```$', '', raw.strip()))
    if not isinstance(value, dict) or value.get('choice') not in TOOLS:
        raise ValueError('unknown choice / not object')
    if not isinstance(value.get('reason'), str) or not value['reason'].strip():
        raise ValueError('missing reason')
    return value


def offline_checks(cases):
    checks, rehearsals = [], []
    assert len(cases) in (2, 3) and len({c['id'] for c in cases}) == len(cases)
    for case in cases:
        for state in STATES:
            env = Environment(case, state)
            known = set(env.facts)
            for record in env.records:
                assert record['id'] not in known and set(record['depends_on']) <= known
                known.add(record['id'])
            trajectory = []
            for step, action in enumerate(case['reference'][state], 1):
                direct = env.payload('direct')
                explicit = env.payload('explicit_impact')
                explicit.pop('依据发生变化、尚待复核的旧判断编号')
                assert direct == explicit  # includes identical histories and tool surfaces
                assert env.expected() == [action], (case['id'], state, step)
                outcome = env.execute(action)
                assert outcome['ok'] and not outcome['unsafe']
                event = env.event(step)
                if event:
                    expected = case['expected_event_review'] if state == 'changed' else []
                    assert event['affected'] == expected
                    if state == 'changed':
                        assert event['preserved'] == case['expected_preserved']
                trajectory.append({'step': step, 'choice': action, 'outcome': outcome, 'event': event})
            assert env.event_fired and env.final_check()['compliant_completion']
            rehearsals.append({'case': case['id'], 'state': state, 'steps': trajectory, 'final': env.final_check()})
            checks.append(f"{case['id']}/{state}: reference, dependency DAG, selective invalidation, arm parity, final effects")
        # Stale continuation must be rejected by both next-step scoring and submit guard.
        changed = Environment(case, 'changed')
        first = case['reference']['changed'][0]
        changed.execute(first)
        changed.event(1)
        assert 'submit' not in changed.expected()
        rejected = changed.execute('submit')
        assert rejected['unsafe'] and not rejected['ok'] and not changed.writes
        assert not changed.final_check()['business_correct']
        # Unnecessary identity work must not be credited as a reasonable next step.
        assert 'repeat_identity' not in changed.expected()
        checks.append(case['id'] + ': stale-submit negative control and unnecessary-recheck rejection')
    address = next(c for c in cases if c['kind'] == 'address')
    env = Environment(address, 'unchanged')
    env.execute('default_address')
    for action in address['reference']['unchanged']:
        env.execute(action)
    assert not env.final_check()['business_correct']
    checks.append('wrong account write cannot pass final-effect scorer even if order later submitted')
    for raw in ('[]', '{"choice":"invented","reason":"x"}', '{"choice":"submit"}'):
        try:
            read_response(raw)
        except (ValueError, TypeError):
            pass
        else:
            raise AssertionError('malformed output accepted')
    checks.append('malformed/unknown/missing-reason output rejected')
    return {'status': 'passed', 'checks': checks, 'reference_rehearsals': rehearsals,
            'note': '离线参考策略不是模型结果，不计入在线正确率。'}


def episode(case, state, arm, trial, client, emit):
    env = Environment(case, state)
    eid = f"{case['id']}/{state}/{arm}/{trial}"
    rows = []
    for step in range(1, MAX_STEPS + 1):
        payload = env.payload(arm)
        messages = [{'role': 'system', 'content': SYSTEM},
                    {'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)}]
        row = {'episode': eid, 'case': case['id'], 'state': state, 'arm': arm, 'trial': trial,
               'step': step, 'messages': messages, 'expected': env.expected(),
               'pending_private': sorted(env.pending)}
        try:
            record = client.chat('pilot_multiturn', messages, max_tokens=240, temperature=0,
                                 thinking=False, retries=0)
            response = record['response']
            row.update(response=response, seconds=round(record['seconds'], 3))
            raw = response['choices'][0]['message'].get('content') or ''
        except Exception as exc:
            matched = re.search(r'Error code: (\d+)', str(exc))
            row.update(status='api_error', error=('HTTP ' + matched[1]) if matched else type(exc).__name__, correct=False)
            rows.append(row)
            emit(row)
            break
        try:
            decision = read_response(raw)
        except (ValueError, TypeError) as exc:
            row.update(status='format_error', error=str(exc), correct=False)
            rows.append(row)
            emit(row)
            break
        row.update(status='ok', **decision, correct=decision['choice'] in row['expected'])
        row['tool_result'] = env.execute(decision['choice'])
        row['external_event'] = env.event(step)
        row['facts_after'] = deepcopy(env.facts)
        rows.append(row)
        emit(row)
        if env.terminal:
            break
    return {'episode': eid, 'case': case['id'], 'state': state, 'arm': arm, 'trial': trial,
            'steps': len(rows), 'correct_steps': sum(r['correct'] for r in rows),
            'all_steps_reasonable': all(r['correct'] for r in rows),
            'post_event_correct': next((r['correct'] for r in rows if r['step'] == 2), False),
            'errors': sum(r['status'] != 'ok' for r in rows),
            'stop_reason': rows[-1]['status'] if rows[-1]['status'] != 'ok' else (env.terminal or 'step_limit'),
            **env.final_check()}


def summarize(out, episodes, traces, planned):
    lines = ['# 第二轮多轮小试结果', '',
             f'模型 `{MODEL}`；计划 {planned} 条轨迹，实际 {len(episodes)} 条、{len(traces)} 次模型调用。', '',
             '|状态|组别|变化/参照后下一步正确|逐步合理|业务终态正确|全程合规办结|违规尝试|接口/格式错误|',
             '|---|---|---:|---:|---:|---:|---:|---:|']
    for state in STATES:
        for arm in ARMS:
            es = [e for e in episodes if e['state'] == state and e['arm'] == arm]
            rs = [r for r in traces if r['state'] == state and r['arm'] == arm]
            lines.append(f'|{state}|{arm}|{sum(e["post_event_correct"] for e in es)}/{len(es)}|'
                         f'{sum(r["correct"] for r in rs)}/{len(rs)}|'
                         f'{sum(e["business_correct"] for e in es)}/{len(es)}|'
                         f'{sum(e["compliant_completion"] for e in es)}/{len(es)}|'
                         f'{sum(e["unsafe_attempts"] for e in es)}|{sum(e["errors"] for e in es)}|')
    lines += ['', '|场景|状态|组别|工具顺序|终态|合规办结|', '|---|---|---|---|---|---|']
    for e in episodes:
        seq = ' → '.join(r.get('choice', r['status']) for r in traces if r['episode'] == e['episode'])
        lines.append(f'|{e["case"]}|{e["state"]}|{e["arm"]}|{seq}|{e["terminal"]}|{e["compliant_completion"]}|')
    lines += ['', '业务终态正确检查实际模拟写入、最新方案及明确告知；全程合规办结还要求无违规尝试。',
              '订单阶段阻断场景中，说明不可修改且没有写入属于合规结束，单独标记 blocked_explained。',
              '逐步合理是依据状态前提的预设操作判定，不评价自然语言理由的充分性；提前失败与步数耗尽计办结失败。',
              '三个手工场景不是独立真实业务样本；不进行显著性检验或能力泛化。']
    (out / 'summary.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--trials', type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    cases = json.loads((HERE / 'scenarios.json').read_text(encoding='utf-8'))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = HERE / ('selfcheck' if args.check else 'results') / stamp
    out.mkdir(parents=True)
    before = protected_hashes()
    dump(out / 'protected_before.json', before)
    report = offline_checks(cases)
    dump(out / 'offline_check.json', report)
    print(f'离线自检通过：{len(report["checks"])} 项，6 条参考演练。', flush=True)
    if args.check:
        assert before == protected_hashes()
        dump(out / 'protected_verification.json', {'unchanged': True, 'files': len(before)})
        print(out, flush=True)
        return
    client_file = ROOT / 'exp2layer' / 'llm.py'
    assert digest(client_file) == digest(FIRST / 'results' / '20261119T175057651633Z' / 'snapshot' / 'llm.py')
    sys.path.insert(0, str(client_file.parent))
    from llm import DeepSeek
    snapshot = out / 'snapshot'
    snapshot.mkdir()
    for name in ('run.py', 'scenarios.json', 'README.md', '方案.md'):
        shutil.copy2(HERE / name, snapshot / name)
    shutil.copy2(client_file, snapshot / 'llm.py')
    # Execute source without importing to avoid creating __pycache__ in protected round one.
    first = {'__file__': str(FIRST / 'run.py'), '__name__': 'round1_snapshot'}
    exec(compile((FIRST / 'run.py').read_text(encoding='utf-8'), str(FIRST / 'run.py'), 'exec'), first)
    assert POLICY == first['POLICY']
    rng = random.Random(71)
    pairs = [(c, s, t) for c in cases for s in STATES for t in range(1, args.trials + 1)]
    rng.shuffle(pairs)
    jobs = [(c, s, a, t) for c, s, t in pairs for a in rng.sample(ARMS, 2)]
    dump(out / 'metadata.json', {
        'requested_model': MODEL, 'sampling': {'temperature': 0, 'thinking': False, 'max_tokens': 240},
        'timeout_seconds': 35, 'retries': 0, 'system_prompt': SYSTEM, 'policy': POLICY, 'tools': TOOLS,
        'max_steps': MAX_STEPS, 'trials': args.trials, 'order_seed': 71, 'planned_episodes': len(jobs),
        'max_calls': len(jobs) * MAX_STEPS, 'execution': 'sequential paired episodes; fresh environment each episode',
        'job_order': [f'{c["id"]}/{s}/{a}/{t}' for c, s, a, t in jobs],
        'snapshot_sha256': {p.name: digest(p) for p in snapshot.iterdir()},
        'client_matches_round1': True, 'policy_matches_round1': True,
    })
    episodes, traces = [], []
    with (out / 'traces.jsonl').open('w', encoding='utf-8') as stream:
        def emit(row):
            traces.append(row)
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
            stream.flush()
            print(f'{row["episode"]} step={row["step"]} {row.get("choice", row["status"])} correct={row["correct"]}', flush=True)
        for case, state, arm, trial in jobs:
            client = DeepSeek(model=MODEL, timeout=35)
            try:
                result = episode(case, state, arm, trial, client, emit)
            finally:
                client.close()
            episodes.append(result)
            dump(out / 'episodes.json', episodes)
            summarize(out, episodes, traces, len(jobs))
            if traces[-1]['status'] == 'api_error':
                break
    after = protected_hashes()
    dump(out / 'protected_verification.json', {'unchanged': before == after, 'files': len(before),
         'changed_paths': [p for p in before.keys() | after.keys() if before.get(p) != after.get(p)]})
    assert before == after, 'protected files changed externally during run'
    dump(out / 'run_status.json', {'complete': len(episodes) == len(jobs), 'episodes': len(episodes),
                                 'calls': len(traces), 'returned_models': sorted({r['response'].get('model', '') for r in traces if 'response' in r})})
    print(out, flush=True)
    if len(episodes) != len(jobs):
        raise SystemExit('接口错误，保留部分结果，停止试跑。')


if __name__ == '__main__':
    main()
