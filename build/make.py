import subprocess, sys, runpy
sys.path.insert(0, 'build')
runpy.run_path('build/build.py')
import artigo4
others = ['proposito-de-vida', 'mente-e-corpo', 'bpm-em-pmes']
artigo4.patch_nav_and_assets(others)
artigo4.build([(s, l) for s, l in [('proposito-de-vida', 'Propósito de vida'), ('mente-e-corpo', 'Mente e corpo'), ('bpm-em-pmes', 'BPM em PMEs'), ('passaporte-pessoa-idosa', 'Pessoa idosa')]])
runpy.run_path('build/home.py')
open('docs/.nojekyll','w').close()
