"""Read-only index/copy of historical source, configurations and selected evidence."""
import os,json,hashlib,shutil,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HIST=Path(os.getenv('DCA_HISTORICAL_ROOT','D:/experimentn/Codex工作区/实验'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 index=['# 前期探索索引（01–23轮）','','本目录是前期探索，不是确证性总榜。基础题、状态变体和重复不混作独立样本。历史原始目录未移动、未重写；归档代码中的绝对路径与冻结清单原样保留，不能假定拷贝后即可在归档目录直接运行。','', '仓库收录代码、配置、摘要和代表轨迹；大批请求/状态/原始轨迹仍在各ARCHIVE.json指向的本地完整档案。复制文件有SHA256，未复制原始档案只登记路径/文件数/体积，不冒称已验证其全部hash。','','|轮次/问题|主要观察（摘录，须结合报告限制）|仓库证据|完整原始档案|','|---|---|---|---|'];overview=[]
 for old in sorted(HIST.iterdir()):
  if not re.match(r'^(0[1-9]|1[0-9]|2[0-2])_',old.name):continue
  number=old.name[:2];dest=ROOT/f'experiments/preliminary/round{number}';dest.mkdir(parents=True,exist_ok=True);copied=[];skipped=[];raw_count=raw_bytes=0
  for p in old.rglob('*'):
   if not p.is_file()or'__pycache__'in p.parts:continue
   rel=p.relative_to(old);parts=rel.parts;size=p.stat().st_size
   if 'results'in parts or'runs'in parts:raw_count+=1;raw_bytes+=size
   select=(p.suffix in('.py','.ps1','.sh')and'results'not in parts and'runs'not in parts)or(any(x in parts for x in ('snapshot','frozen_inputs'))and p.suffix in('.py','.json','.md'))or('configs'in parts and p.suffix in('.json','.md','.toml','.yaml','.yml'))or(p.suffix=='.md'and p.name in('README.md','PROTOCOL.md','RESULTS.md','PAIRED_RESULTS.md','FIRST_DECISION_PAIRS.md','CONTINUATION_PAIRS.md','summary.md','结果解读.md','工程记录.md'))
   if not select:continue
   if size>2_000_000:skipped.append({'path':str(p),'bytes':size,'reason':'large artifact kept at original path'});continue
   content=p.read_bytes()
   if re.search(rb'sk-[A-Za-z0-9_-]{20,}',content):skipped.append({'path':str(p),'bytes':size,'reason':'potential credential: omitted from Git copy; original untouched'});continue
   target=dest/'archive'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);copied.append({'original':str(p),'copy':str(target.relative_to(ROOT)),'sha256':digest(p),'bytes':size})
  traces=sorted([p for p in old.rglob('*.md')if('TRACE'in p.name.upper()or'TRACE'in str(p.parent).upper())and p.stat().st_size<300000],key=lambda p:(len(p.parts),len(p.name)))
  if traces:
   p=traces[0];target=dest/'representative'/p.name;target.parent.mkdir(exist_ok=True);shutil.copy2(p,target);copied.append({'original':str(p),'copy':str(target.relative_to(ROOT)),'sha256':digest(p),'bytes':p.stat().st_size})
  reports=sorted([p for p in old.rglob('RESULTS.md')if p.stat().st_size<2_000_000],key=lambda p:len(p.parts));report=reports[0]if reports else old/'README.md';excerpt='待结合原始报告核对，索引不推断额外结论。'
  if report.exists():
   text=report.read_text('utf-8-sig');lines=[s.strip().replace('|','／')for s in text.splitlines()if s.strip()and not s.startswith(('#','|','```'))];excerpt=' '.join(lines[:2])[:220]
   if number=='01':excerpt='首轮单步对照两组均16/16；未观察到正确率差，成为多轮/同状态续行探索起点。详见各运行summary与冻结snapshot。'
   elif number=='02':excerpt='12条轨迹、40次调用；两组各20/20步合理、6/6业务合规结束，无正确率收益证据。'
   elif number=='03':excerpt='两组均完成算新差价、重新确认、两件一次提交；框架额外5次状态维护，来源/依赖仍有缺口。'
   elif number=='04':excerpt='15项离线验收与精确回放通过；单状态开发观察不能证明稳定首步偏好。'
   elif number=='05':excerpt='一次开发观察中较省首步随库存证据变化；早期先问分支失败保留，不构成稳定收益。'
   elif number=='13':excerpt='正式4条：3条登记、1条尊重实际拒绝停止；另有模拟偏离与范围待核实，无完整同质量配对。'
   elif number=='15':excerpt='8条中6登记、2无可用响应；31次无usage异常；完整质量4通过、2理由有误、2未观察。'
  manifest={'round':number,'original_root':str(old),'original_paths_preserved':True,'copied_files':copied,'not_copied_selected_large_or_sensitive':skipped,'bulk_raw_archive':{'root':str(old/'results'),'files':raw_count,'bytes':raw_bytes,'git_storage':'external original directory, not moved'}};(dest/'ARCHIVE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
  (dest/'README.md').write_text(f'# 第{number}轮：{old.name[3:]}\n\n问题主题：{old.name[3:]}。\n\n观察摘录：{excerpt}\n\n原始档案：`{old}`。复制文件与SHA256见[ARCHIVE.json](ARCHIVE.json)。历史冻结记录及路径依赖原样保存。',encoding='utf-8')
  index.append(f'|{number} {old.name[3:]}|{excerpt}|[目录](round{number}/README.md)|`{old}`|');overview.append({'round':number,'report':str(report),'excerpt':excerpt})
 index+=['|23 三模块闭环修复与同状态续行|先验收旧题，再独立新题试采；正式结果和局限以本轮报告为准。|[本轮](round23-framework-loop/RESULTS.md)|原始请求路径见本轮归档清单|','','研究问题与三个模块依据见[研究定位](../../docs/research_basis.md)，逐轮决定见[研究日志](../../docs/research_log.md)。']
 (ROOT/'experiments/preliminary/README.md').write_text('\n'.join(index),encoding='utf-8');(ROOT/'docs/history_index_sources.json').write_text(json.dumps(overview,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
