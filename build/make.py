import subprocess, sys, runpy
sys.path.insert(0, 'build')
runpy.run_path('build/build.py')
import artigo4
others = ['proposito-de-vida', 'mente-e-corpo', 'bpm-em-pmes']
artigo4.patch_nav_and_assets(others)
import animar
artigo4.build([(s, l) for s, l in [('proposito-de-vida', 'Propósito de vida'), ('mente-e-corpo', 'Mente e corpo'), ('bpm-em-pmes', 'BPM em PMEs'), ('passaporte-pessoa-idosa', 'Transformação de Serviço'), ('pmbok-dialetica', 'Evolução do PMBOK')]])
for _s in others:
    animar.patch(_s)
import os, shutil
os.makedirs('docs/pmbok-dialetica', exist_ok=True)
shutil.copy('src/orig/pmbok-dialetica/index.html', 'docs/pmbok-dialetica/index.html')
for _f in os.listdir('src/orig/pmbok-dialetica/img'):
    shutil.copy('src/orig/pmbok-dialetica/img/' + _f, 'docs/assets/img/' + _f)
shutil.copy('src/orig/pmbok-dialetica/Evolucao_Dialetica_Gerenciamento_Projetos_v3.pdf', 'docs/assets/pdf/')
runpy.run_path('build/home.py')
runpy.run_path('build/projetos.py')
open('docs/.nojekyll','w').close()
