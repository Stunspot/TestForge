#!/usr/bin/env python3
"""Verify the accepted current bundle against maintained inputs; retain historical seals."""
from pathlib import Path
import hashlib,io,json,sys,tempfile,zipfile
from build_public_release import DOCS, HANDLES, assert_unlinked
from verify_family_release import verify
ROOT=Path(__file__).resolve().parents[1]
def digest(b):return hashlib.sha256(b).hexdigest()
def tree(root):
    assert_unlinked(root)
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'}}
def main():
    meta=json.loads((ROOT/'verification/estate-root-review/CURRENT-RELEASE.json').read_text(encoding='utf-8'))
    archive=ROOT/meta['archive'];assert digest(archive.read_bytes())==meta['sha256'],'Accepted artifact hash differs'
    with zipfile.ZipFile(archive) as z:
        members={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
        assert len(members)==len([n for n in z.namelist() if not n.endswith('/')]),'Duplicate ZIP members'
        prefix='testforge-v2.0.0/'
        assert all(n.startswith(prefix) and '..' not in Path(n).parts for n in members),'Unexpected ZIP path'
        packed={n[len(prefix):]:b for n,b in members.items()}
        for handle in HANDLES:
            source=tree(ROOT/'plugins/testforge/skills'/handle)
            key='codex/testforge/skills/'+handle+'/'
            actual={n[len(key):]:b for n,b in packed.items() if n.startswith(key)}
            assert actual==source,'Accepted runtime differs from canonical source: '+handle
            assert tree(ROOT/'testforge/skills'/handle)==source,'Current runtime mirror differs: '+handle
            with zipfile.ZipFile(ROOT/'claude-ai'/f'{handle}-v2.0.0.zip') as inner:
                assert {n[len(handle)+1:]:inner.read(n) for n in inner.namelist() if not n.endswith('/')}==source,'Current Claude mirror differs: '+handle
        plugin=tree(ROOT/'plugins/testforge')
        assert {n[len('codex/testforge/'):]:b for n,b in packed.items() if n.startswith('codex/testforge/')}==plugin,'Plugin metadata/source differs'
        for name in DOCS:
            expected=(ROOT/'release-docs'/name).read_text(encoding='utf-8').replace('../releases/v2.0.0/','../').encode('utf-8')
            assert packed['docs/'+name]==expected,'Accepted customer document differs: '+name
        assert packed['tools/verify_release.py']==(ROOT/'tools/verify_family_release.py').read_bytes(),'Verifier differs'
        assert packed['LICENSE.md']==(ROOT/'LICENSE.md').read_bytes(),'License differs'
        with tempfile.TemporaryDirectory(prefix='testforge-current-',dir=ROOT.parent.resolve()) as temp:
            native=Path(temp)
            for name,data in packed.items():
                target=native/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            result=verify(native)
            assert result['ok'],result
            print(json.dumps(result,sort_keys=True))
    print('PASS: current source, runtime mirrors, customer guidance and accepted native artifact agree; historical seals retained')
if __name__=='__main__':main()
