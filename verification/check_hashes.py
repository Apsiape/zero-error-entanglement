"""Check LF hash list and source-manifest entries against the shipped files."""
from pathlib import Path, PurePosixPath
import hashlib, json, sys
root=Path(__file__).resolve().parent.parent
manifest=root/'verification/SHA256SUMS'
raw=manifest.read_bytes()
assert b'\r' not in raw and raw.endswith(b'\n'), 'SHA256SUMS must use LF line endings.'
failed=[]
count=0
def check(expected,name):
    rel=PurePosixPath(name)
    assert not rel.is_absolute() and '..' not in rel.parts and ':' not in name and '\\' not in name
    path=root/name
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==expected
for line in raw.decode('utf-8').splitlines():
    expected,name=line.split('  ',1)
    count+=1
    if not check(expected,name):failed.append(name)
source=json.loads((root/'paper/source-manifest.json').read_text(encoding='utf-8'))
for entry in source['files']:
    if not check(entry['sha256'],entry['path']):failed.append(entry['path'])
if failed:
    print('FAIL: '+', '.join(sorted(set(failed))));sys.exit(1)
print(f"PASS: SHA256SUMS {count}/{count}; source manifest {len(source['files'])}/{len(source['files'])}; LF line endings")
