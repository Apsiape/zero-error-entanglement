"""Extract the archive afresh; verify hashes, finite checks and a clean rebuild."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, subprocess, sys, tempfile, zipfile
root=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-directory',type=Path)
args=parser.parse_args()
dest=args.output_directory.resolve() if args.output_directory else Path(tempfile.mkdtemp(prefix='source-check-'))
dest.mkdir(parents=True,exist_ok=True)
if any(dest.iterdir()):raise SystemExit('Output directory must be empty.')
archive=root/'paper/source.zip'
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and ':' not in n and '\\' not in n for n in z.namelist())
    z.extractall(dest)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
results=[]
for label,argv in [
 ('hashes',['verification/check_hashes.py']),
 ('finite_checks',['verification/run_all.py','--output-directory','fresh-checks']),
 ('fresh_build',['paper/build.py','--output-directory','fresh-build']),
 ('hashes_after_build',['verification/check_hashes.py'])]:
    run=subprocess.run([sys.executable,'-B',*argv],cwd=dest,text=True,encoding='utf-8',capture_output=True,env=env)
    (dest/(label+'.out')).write_text(run.stdout+run.stderr,encoding='utf-8',newline='\n')
    results.append(dict(step=label,passed=run.returncode==0,exit_code=run.returncode))
    print(('PASS' if run.returncode==0 else 'FAIL')+': extracted '+label,flush=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
same=(dest/'fresh-build/main.pdf').is_file() and sha(dest/'fresh-build/main.pdf')==sha(dest/'paper/main.pdf')
results.append(dict(step='rebuilt_pdf_byte_identity',passed=same))
print(('PASS' if same else 'FAIL')+': rebuilt PDF byte identity')
summary=dict(archive_sha256=sha(archive),passed=all(x['passed'] for x in results),results=results)
(dest/'portability.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Results: '+str(dest))
sys.exit(0 if summary['passed'] else 1)
