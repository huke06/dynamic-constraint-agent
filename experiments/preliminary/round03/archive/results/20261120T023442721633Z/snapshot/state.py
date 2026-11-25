"""Domain-neutral, versioned evidence graph. No task IDs or action oracle."""
from copy import deepcopy


class EvidenceState:
    def __init__(self):
        self.facts = {}
        self.judgments = {}
        self.transitions = []

    def snapshot(self):
        return {'facts': deepcopy(self.facts), 'judgments': deepcopy(self.judgments)}

    def apply(self, patch, message_count):
        previous = self.snapshot()
        facts, judgments = deepcopy(self.facts), deepcopy(self.judgments)
        changed = set()
        touched = set()

        def sources(entry):
            refs = entry.get('sources', [])
            if not refs or any(type(x) is not int or not 0 <= x < message_count for x in refs):
                raise ValueError('missing/invalid source message index')
            return refs

        for entry in patch.get('facts', []):
            key = entry['id']
            if not key.startswith('f.'):
                raise ValueError('fact IDs must start f.')
            refs = sources(entry)
            old = facts.get(key)
            version = old['version'] if old else 0
            if old is None or old['value'] != entry['value']:
                changed.add(key)
                version += 1
            facts[key] = {'value': entry['value'], 'sources': refs, 'version': version}

        def descendants(keys):
            result = set()
            while True:
                new = {key for key, record in judgments.items()
                       if set(record['depends_on']) & (set(keys) | result)} - result
                if not new:
                    return result
                result.update(new)

        stale = descendants(changed)
        for key in stale:
            judgments[key]['status'] = 'stale'
        for entry in patch.get('judgments', []):
            key = entry['id']
            if not key.startswith('j.') or entry['status'] not in ('supported', 'unknown'):
                raise ValueError('invalid judgment ID/status')
            refs = sources(entry)
            if not entry.get('depends_on'):
                raise ValueError('judgments need explicit dependencies')
            old = judgments.get(key)
            semantic = {k: entry[k] for k in ('text', 'depends_on', 'status')}
            differs = old is None or any(old[k] != semantic[k] for k in semantic)
            judgments[key] = {**semantic, 'sources': refs,
                              'version': (old['version'] if old else 0) + int(differs)}
            if differs:
                changed.add(key)
            touched.add(key)
        stale.update(descendants(changed))
        for key in stale - touched:
            judgments[key]['status'] = 'stale'

        done, visiting = set(facts), set()

        def visit(key):
            if key in done:
                return
            if key in visiting or key not in judgments:
                raise ValueError('cycle or unknown dependency: ' + key)
            visiting.add(key)
            record = judgments[key]
            for dep in record['depends_on']:
                visit(dep)
                if dep in judgments and judgments[dep]['status'] != 'supported':
                    if record['status'] == 'supported':
                        record['status'] = 'stale'
            record['dependency_versions'] = {
                dep: (facts.get(dep) or judgments[dep])['version'] for dep in record['depends_on']}
            visiting.remove(key)
            done.add(key)

        for key in judgments:
            visit(key)
        if len(facts) > 128 or len(judgments) > 64:
            raise ValueError('state size limit exceeded')
        self.facts, self.judgments = facts, judgments
        transition = {'patch': deepcopy(patch), 'changed': sorted(changed),
                      'affected_including_refreshed': sorted(stale),
                      'still_stale': sorted(k for k, r in judgments.items() if r['status'] == 'stale'),
                      'before': previous, 'after': self.snapshot()}
        self.transitions.append(transition)
        return transition
