"""Build a fresh PDF with pdfLaTeX and BibTeX, preserving the shipped PDF."""
from pathlib import Path
import argparse, os, subprocess, sys, tempfile

root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-directory', type=Path)
args=parser.parse_args()
build=(args.output_directory.resolve() if args.output_directory else Path(tempfile.mkdtemp(prefix='paper-build-')))
build.mkdir(parents=True,exist_ok=True)
if any(build.iterdir()):
    raise SystemExit('Output directory must be empty for a clean build.')
env=dict(os.environ,SOURCE_DATE_EPOCH='1793664000',FORCE_SOURCE_DATE='1')
latex=['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory='+str(build),'main.tex']
commands=[latex,['bibtex',str(build/'main')],latex,latex]
for i,cmd in enumerate(commands,1):
    run=subprocess.run(cmd,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
    (build/('pass-'+str(i)+'.txt')).write_text(run.stdout,encoding='utf-8',newline='\n')
    if run.returncode:
        print(run.stdout[-9000:]);sys.exit(run.returncode)
log=(build/'main.log').read_text(encoding='utf-8',errors='replace')
bad=[line for line in log.splitlines() if any(x in line for x in ['Warning','Overfull','Underfull','undefined references','undefined citations'])]
blg=(build/'main.blg').read_text(encoding='utf-8',errors='replace')
bad += [line for line in blg.splitlines() if 'Warning' in line or 'error message' in line]
if bad:
    print('\n'.join(bad));sys.exit(2)
print('PASS: pdfLaTeX + BibTeX; final logs contain no warnings, undefined references or box diagnostics.')
print('Built PDF: '+str(build/'main.pdf'))
print('The shipped main.pdf was preserved.')
