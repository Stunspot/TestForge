from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
r=Path(__file__).resolve().parents[2];ev=Path(__file__).parent
paths=[]
for base in ['plugins/testforge','release-docs','delivery']:
 paths += [p.relative_to(r) for p in (r/base).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += [Path(x) for x in ['.gitattributes','LICENSE.md','tools/build_public_release.py','tools/archive_paths.py','tools/source_text_policy.py','tools/verify_family_release.py','verification/shared-async-revisit/build-candidate.py','releases/estate-quality-20261006-r5/TestForge-v2.0.0.zip']]
paths=sorted(set(paths));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,cwd):return subprocess.run(args,cwd=cwd,text=True,encoding='utf-8',capture_output=True,check=True)
# Disposable local Git test, not a new product or GitHub repository.
with tempfile.TemporaryDirectory(prefix='testforge-async-checkout-',dir=r.parent.resolve()) as temporary:
 base=Path(temporary).resolve();assert base.parent==r.parent.resolve();source=base/'source';checkout=base/'checkout';source.mkdir()
 for rel in paths:
  dest=source/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(r/rel,dest)
 run(['git','init','--initial-branch=codex/async-fixture'],source);run(['git','config','core.autocrlf','true'],source);run(['git','add','--all'],source)
 run(['git','-c','user.name=TestForge local fixture','-c','user.email=fixture@example.invalid','commit','-m','Isolated exact candidate inputs'],source)
 run(['git','clone','--no-hardlinks','--no-local','--config','core.autocrlf=true',str(source),str(checkout)],base)
 mismatches=[str(rel) for rel in paths if (checkout/rel).read_bytes()!=(r/rel).read_bytes()];assert not mismatches,mismatches
 target=checkout/'releases/async-rebuild';p=run([sys.executable,'-B','-X','utf8',str(checkout/'verification/shared-async-revisit/build-candidate.py'),'--output-dir',str(target)],checkout);result=json.loads(p.stdout)
 original=r/'releases/estate-quality-20261007-r6/TestForge-v2.0.0.zip';assert sha(target/original.name)==sha(original)
 report={'ok':True,'scope':'Actual local Git add, commit and clone checkout under existing LF policy with core.autocrlf=true; private deterministic native rebuild','selected_files':len(paths),'byte_mismatches':mismatches,'candidate_sha256':sha(original),'rebuilt_sha256':sha(target/original.name),'native_verifier':result['native_verifier'],'selected_paths':[str(p).replace('\\','/') for p in paths]}
 (ev/'git-checkout-parity.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({k:v for k,v in report.items() if k!='selected_paths'},indent=2))