from pathlib import Path
import ast,hashlib,io,json,re,shutil,subprocess,sys,zipfile
r=Path(__file__).resolve().parents[2];ev=Path(__file__).parent;a=Path('E:/Indranet/Nova/projects/project-records/projects/augment-estate-quality-repair/records/product-audits/testforge/shared-async-revisit');out=r/'releases/estate-quality-20261007-r6';zpath=out/'TestForge-v2.0.0.zip';old=r/'releases/estate-quality-20261006-r5/TestForge-v2.0.0.zip'
sys.path.insert(0,str(r/'tools'));from rebuild_public_release import write_zip
from source_text_policy import assert_source_text
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
# Preserve current mirrors before their only generated changes.
for handle in ['software-verification','verification-reviewer']:
 p=r/'claude-ai'/f'{handle}-v2.0.0.zip';dest=a/'mirror-before'/p.name;dest.parent.mkdir(exist_ok=True);assert not dest.exists();shutil.copy2(p,dest);write_zip(r/'testforge/skills'/handle,p,handle)
with zipfile.ZipFile(zpath) as z,zipfile.ZipFile(old) as base:
 current={n:z.read(n) for n in z.namelist()};before={n:base.read(n) for n in base.namelist()};delta=[]
 for n in sorted(current.keys()|before.keys()):
  if current.get(n)!=before.get(n):delta.append({'path':n,'change':'added' if n not in before else 'changed','before_sha256':hashlib.sha256(before[n]).hexdigest() if n in before else None,'after_sha256':hashlib.sha256(current[n]).hexdigest()})
 assert len(delta)==7,delta
 assert not any('/scripts/' in row['path'] or '/docs/' in row['path'] or '/assets/' in row['path'] or row['path'].endswith('/SKILL.md') for row in delta)
 for handle in ['software-verification','verification-reviewer']:
  sr=r/'plugins/testforge/skills'/handle;source={p.relative_to(sr).as_posix():p.read_bytes() for p in sr.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
  prefix=f'testforge-v2.0.0/codex/testforge/skills/{handle}/';packed={n[len(prefix):]:b for n,b in current.items() if n.startswith(prefix)};assert packed==source
  mr=r/'testforge/skills'/handle;assert {p.relative_to(mr).as_posix():p.read_bytes() for p in mr.rglob('*') if p.is_file() and '__pycache__' not in p.parts}==source
  with zipfile.ZipFile(r/'claude-ai'/f'{handle}-v2.0.0.zip') as inner:assert {n[len(handle)+1:]:inner.read(n) for n in inner.namelist()}==source
 save(ev/'source-package-parity.json',{'ok':True,'canonical_runtime_files':114,'claude_archives':2,'delta':delta,'no_executable_metadata_schema_customer_doc_or_art_change':True})
# Existing scanner findings are compared by path relative to each native skill root.
scanner=Path('C:/Users/user/.codex/skills/omnicompetence/scripts/validate_candidate.py');scanner_results=[]
for handle in ['software-verification','verification-reviewer']:
 roots=[r/'plugins/testforge/skills'/handle,r/'verification/estate-quality-20261006/r5/native-extract/testforge-v2.0.0/codex/testforge/skills'/handle];reports=[]
 for root in roots:
  proc=subprocess.run([sys.executable,'-B','-X','utf8',str(scanner),str(root),'--json'],capture_output=True,text=True,encoding='utf-8');d=json.loads(proc.stdout)
  for f in d['findings']:f['path']=Path(f['path']).relative_to(root).as_posix()
  reports.append(d['findings'])
 assert reports[0]==reports[1],reports
 scanner_results.append({'handle':handle,'new_findings':[],'retained_r5_findings':reports[0],'boundary':'Current static scanner findings predate this delta; do not imply whole source scan clean.'})
save(ev/'scanner-comparison.json',scanner_results)
# Follow the new local resources at the same package boundary the model receives.
changed=[r/'plugins/testforge/skills/software-verification/references/specialized/customer-journeys.md',r/'plugins/testforge/skills/software-verification/references/reliability/concurrency-and-races.md',r/'plugins/testforge/skills/software-verification/examples/pending-replacement/walkthrough.md',r/'plugins/testforge/skills/verification-reviewer/customer-journeys.md']
links=[]
for p in changed:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  dest=(p.parent/target).resolve();assert dest.is_file(),(p,target);assert dest.is_relative_to(r/'plugins/testforge/skills');links.append({'source':p.relative_to(r).as_posix(),'target':dest.relative_to(r).as_posix()})
assert_source_text(changed+list(ev.glob('*.py'))+list(ev.glob('*.cjs'))+[ev/'fixture.html'])
save(ev/'changed-resource-check.json',{'ok':True,'resolved_links':links,'all_changed_authored_text':'UTF-8 LF'})
print(json.dumps({'runtime_parity':114,'package_delta':len(delta),'new_static_findings':0,'retained_static_findings':len(scanner_results[0]['retained_r5_findings'])}))