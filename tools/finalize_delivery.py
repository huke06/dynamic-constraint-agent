"""Finalize navigation and append-only research log; no model calls."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'experiments/preliminary/round23-framework-loop'
V = E / 'versions/v2'
for name in ('FIRST_DECISION_PAIRS.md', 'CONTINUATION_PAIRS.md'):
    prior = E / 'results' / ('V1_' + name)
    if not prior.exists():
        shutil.copyfile(E / name, prior)
    shutil.copyfile(V / name, E / name)
for name in ('TRACE_old_t93_conflict_r1.md', 'TRACE_B_t26_conflict_r2_analyze.md', 'TRACE_B_t26_conflict_r2_clarify.md'):
    shutil.copyfile(V / name, E / name)
(E / 'README.md').write_text('''# 第23轮导航

当前验收版本为独立冻结的v2：[结果](RESULTS.md)、[状态前后](STATE_TRANSITIONS.md)、[首步配对](FIRST_DECISION_PAIRS.md)、[续行配对](CONTINUATION_PAIRS.md)、[完整三模块轨迹](TRACE_old_t93_conflict_r1.md)。

源代码见仓库src/dynamic_constraint_agent_v2，配置和冻结见versions/v2/configs，正式结果见versions/v2/results。根目录configs/results及src/dynamic_constraint_agent对应保留的v1，不是当前默认验收结果；v1原首步/续行表保存在results/V1_*.md。v1验收门槛遗漏及修订过程必须与最终结果一起阅读。

大批原始记录留在原位置及独立归档，不纳入Git：[位置与hash](RAW_ARCHIVES.json)。示范和比较仅列为[待审核候选](LEARNING_CANDIDATES.json)，没有训练或可直接使用的偏好标签。
''', encoding='utf-8')
(V / 'RESULTS.md').write_text('''# 独立冻结v2结果

完整汇总：[本轮RESULTS.md](../../RESULTS.md)。v2旧题8/8严格通过；新题A两组首步类型/对象均8/8适切，含理由及实际语义执行的严格质量直接5/8、候选8/8；新题B正确登记8/8、严格质量7/8，3对可比较。只有26题两次质量可比且成本方向一致，软属性保持不同，不给出无条件偏好方向。

[首步表](FIRST_DECISION_PAIRS.md) · [续行表](CONTINUATION_PAIRS.md) · [事实复核](results/FACT_REVIEW.json) · [冻结](configs/FREEZE.json)。本版本正式8条旧题+16条首步+8条续行，联调2条另记。v1记录保留，不合并估计收益。
''', encoding='utf-8')

log_path = Path('D:/experimentn/Codex工作区/实验/研究计划与实验日志.md')
marker = '### 2026-11-25 · 第23轮：闭环修复与独立实例轨迹试采'
entry = '''

### 2026-11-25 · 第23轮：闭环修复与独立实例轨迹试采

- **定位与目录。** 沿用2.1两问及状态约束与建模、认知决策、任务执行与反馈三个模块。GitHub空仓库访问及克隆成功，独立组织在D:/experimentn/dynamic-constraint-agent-round23；01–22轮原目录与冻结不变，可复现选件1473份逐文件核对hash。完整原始档案位置另列，不冒称已上传。
- **版本和流程偏差。** v1旧题硬结果通过后提前启动新题，后续逐句话术审阅发现cap不可行被说成无货等错误；这是严格准入遗漏。保留v1正式32条及失败，另冻v2。v2将可判定澄清事实程序化，增加当前/替代逐字段比较；11、16已被诊断，换用未参与本轮调试的26、35题。v2离线11个回归方法及2条联调通过，旧题逐条严格通过后才启动新题。v1与v2各32条正式，另8条联调，不合并估计修复收益。
- **旧题闭环。** v2旧8条严格通过：93两起点各两次的预定分析/澄清首步可执行，空可行集成为有效反馈；后续自主读新许可，重新整单授权并正确登记。29两次局部变更保留另一商品依据，无重复解析；102两次在程序核定撤回后的快照重新取得当前授权。102不代表自由文本撤回语义能力。
- **独立新实例。** 26、35均为原退货任务的两商品换货受控改编，原题与子任务、状态变体分开存档。A共16条，两组首步类型/对象均8/8适切；冲突时分析/澄清，可行时拟案。全链首步严格质量直接5/8、候选8/8：包含理由虚构分析必需前提、语义分析误读冲突原因，不能据此声称候选提高了类型适切率。
- **同状态续行。** B共8条均正确登记，7条严格通过，3对可比较。26两次均先澄清5次请求、先分析7次；但分析更保留软规格，先澄清更省调用，效用未定义，偏好方向留空。35一条金额参照含糊待核实，不构成两次稳定全质量证据。
- **账本与候选。** 全阶段386次API请求，返回deepseek-flash，均有usage，无网络/解析终止；v1联调循环失败保留。模拟用户为程序，API用量0，编排会话成本未知另列。52条自主下一工作仅为示范候选，26一组为有条件比较候选，无训练或chosen/rejected标签。当前审阅非独立盲审。
- **决定。** 在受控范围内93闭环验收通过；暂不扩采训练数据。先把程序核定的当前整单差额及明确冲突原因传给局部语义分析，补结束/拒绝回归、独立事实复核与软偏好效用定义，再复验新实例。按基础题划分数据。官方Agent端到端比较沿21轮定位另批，不混入本轮。
- **证据。** [第23轮完整报告](D:/experimentn/dynamic-constraint-agent-round23/experiments/preliminary/round23-framework-loop/RESULTS.md)、同目录STATE_TRANSITIONS.md、FIRST_DECISION_PAIRS.md、CONTINUATION_PAIRS.md与完整三模块轨迹；RAW_ARCHIVES.json记录原件/外部副本hash。
'''
old = log_path.read_text(encoding='utf-8-sig')
if marker not in old:
    with log_path.open('a', encoding='utf-8') as f:
        f.write(entry)
updated = log_path.read_text(encoding='utf-8-sig')
updated = updated.replace('21_动态约束复验与框架优化/results/RESULTS.md', '../experiments/preliminary/round21/archive/results/RESULTS.md')
updated = updated.replace('22_状态驱动决策与同状态续行/results/RESULTS.md', '../experiments/preliminary/round22/archive/results/RESULTS.md')
updated = updated.replace('D:/experimentn/dynamic-constraint-agent-round23/experiments/preliminary/round23-framework-loop/RESULTS.md', '../experiments/preliminary/round23-framework-loop/RESULTS.md')
(ROOT / 'docs/research_log.md').write_text(updated, encoding='utf-8')

basis = ROOT / 'docs/research_basis.md'
basis.write_text(basis.read_text(encoding='utf-8').replace('新题11/16原业务是退货', 'v1新题11/16、v2独立新题26/35原业务均是退货'), encoding='utf-8')
proposal = Path('D:/experimentn/Codex工作区/申报与文献/当前申报/2027创新类计划项目申报书_分页紧凑版.docx')
(ROOT / 'docs/sources/proposal_basis.json').write_text(json.dumps({
    'source': str(proposal), 'sha256': hashlib.sha256(proposal.read_bytes()).hexdigest(),
    'section': '2.1', 'access': 'read-only',
    'questions': ['Agent如何依据动态业务状态合理开展认知决策？', '如何利用执行反馈评价并提升Agent的认知决策能力？'],
    'note': '当前分页紧凑版docx为依据；不修改申报书，不以较旧正文Markdown替代。'
}, ensure_ascii=False, indent=2), encoding='utf-8')
print('Final navigation written; research log appended once; proposal read-only provenance saved.')
