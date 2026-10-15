"""Captura a tela inicial de cada projeto com o Chrome headless e salva em projetos-ia/img/<slug>.jpg.
Uso: python build/capturas.py [pasta_projetos-ia]"""
import os, subprocess, sys, tempfile
sys.path.insert(0, 'build')
from projetos_data import PROJ
from slug import slug
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join('..', 'projetos-ia')
EDGE = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
from PIL import Image
for c, n, p, u, d in PROJ:
    png = os.path.join(tempfile.gettempdir(), slug(n) + '.png')
    if os.path.exists(png): os.remove(png)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--user-data-dir=' + os.path.join(tempfile.gettempdir(), 'capchrome'), '--hide-scrollbars', '--window-size=1280,800',
                    '--virtual-time-budget=12000', '--screenshot=' + png, u], capture_output=True, timeout=90)
    if not os.path.exists(png):
        print('FALHOU', n); continue
    im = Image.open(png).convert('RGB').resize((800, 500), Image.LANCZOS)
    im.save(os.path.join(OUT, 'img', slug(n) + '.jpg'), quality=82, optimize=True)
    print('ok', n)
