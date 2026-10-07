"""Private reproducible candidate only; does not seal, accept or update delivery authority."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parents[2]
def build(root,out):
 sys.path.insert(0,str(root/'tools'))
 import build_public_release as b
 if out.exists():raise RuntimeError('Preserve prior outputs: choose a new directory')
 if out.parent.resolve()!=(root/'releases').resolve():raise RuntimeError('Candidate must be directly under this repository releases')
 b.assert_unlinked(root/'plugins/testforge');b.assert_unlinked(root/'release-docs')
 b.assert_source_text(b.files(root/'plugins/testforge')+b.files(root/'release-docs')+[root/'LICENSE.md',root/'tools/verify_family_release.py'])
 out.mkdir(parents=True);shutil.copytree(root/'plugins/testforge',out/'codex/testforge',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
 for name in ['claude','docs','tools']:(out/name).mkdir()
 for name in b.DOCS:
  text=(root/'release-docs'/name).read_text(encoding='utf-8').replace('../releases/v2.0.0/','../')
  (out/'docs'/name).write_text(text,encoding='utf-8',newline='\n')
 shutil.copy2(root/'LICENSE.md',out/'LICENSE.md');shutil.copy2(root/'tools/verify_family_release.py',out/'tools/verify_release.py')
 baseline=root/'releases/estate-quality-20261006-r5/TestForge-v2.0.0.zip'
 if hashlib.sha256(baseline.read_bytes()).hexdigest()!='f5f7348a15fe9407acd63cb55e361c2777510919201c447f2a6f54c9f2b1db68':raise RuntimeError('Accepted r5 baseline changed')
 with zipfile.ZipFile(baseline) as z:manifest=json.loads(z.read('testforge-v2.0.0/manifest.json'))
 manifest['source_records']=[];manifest['claude_archives']=[]
 for handle in b.HANDLES:
  source=out/'codex/testforge/skills'/handle;manifest['source_records'].append(b.source_record(handle,source))
  archive=out/'claude'/f'{handle}-v2.0.0.zip';b.zip_tree(source,archive)
  manifest['claude_archives'].append({'file':'claude/'+archive.name,'handle':handle,'sha256':b.digest(archive.read_bytes())})
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
 check=subprocess.run([sys.executable,'-B','-X','utf8',str(out/'tools/verify_release.py'),str(out)],capture_output=True,text=True,check=True)
 archive=out/'TestForge-v2.0.0.zip';b.zip_tree(out,archive,'testforge-v2.0.0')
 # Four-part candidate companions remain outside native ZIP, as in the accepted format.
 for name in ['TestForge.png','TestForge v2.0.0.md','TestForge v2.0.0 Extra.md']:shutil.copy2(root/'delivery'/name,out/name)
 return {'artifact':str(archive),'sha256':b.digest(archive.read_bytes()),'native_verifier':json.loads(check.stdout),'boundary':'private candidate, no acceptance or release seal'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args();print(json.dumps(build(ROOT,args.output_dir),indent=2))