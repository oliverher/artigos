import re, os, shutil, subprocess
B='https://artigos-oliverher.lovable.app'
O='src/orig'; S='docs'
shutil.rmtree(S,ignore_errors=True)
os.makedirs(S+'/assets/img'); os.makedirs(S+'/assets/pdf')
shutil.copy(O+'/styles.css',S+'/assets/styles.css')
for f in os.listdir(O+'/img'): shutil.copy(O+'/img/'+f,S+'/assets/img/'+f)
pages=['proposito-de-vida','mente-e-corpo','bpm-em-pmes']
for p in pages:
    h=open(f'{O}/{p}.html',encoding='utf8').read()
    for url in sorted(set(re.findall(r'/__l5e/[^"\')\s]+',h))):
        name=url.rsplit('/',1)[1]
        sub='pdf' if name.endswith('.pdf') else 'img'
        dest=f'{S}/assets/{sub}/{name}'
        if not os.path.exists(dest):
            subprocess.run(['curl','-s',B+url,'-o',dest],check=True)
        h=h.replace(url,f'../assets/{sub}/{name}')
    h=re.sub(r'<script\b.*?</script>','',h,flags=re.S)
    h=re.sub(r'<link[^>]*rel="(modulepreload|preload)"[^>]*>','',h)
    h=re.sub(r'<style>(?:(?!</style>).)*lovable-badge(?:(?!</style>).)*</style>','',h,flags=re.S)
    h=re.sub(r'<aside\s[^>]*id="lovable-badge".*?</aside>','',h,flags=re.S)
    h=re.sub(r'<meta name="(author|twitter:site)" content="@?Lovable"/>','',h)
    h=re.sub(r'<link rel="icon"[^>]*>','',h)
    h=h.replace('/assets/styles-DBp-cSl-.css','../assets/styles.css')
    h=h.replace('href="/"','href="../"')
    for q in pages: h=h.replace(f'href="/{q}"',f'href="../{q}/"')
    h=h.replace('</body>','<script src="../assets/app.js"></script></body>')
    os.makedirs(f'{S}/{p}',exist_ok=True)
    open(f'{S}/{p}/index.html','w',encoding='utf8').write(h)
    print(p,len(h),'leftover /__l5e:',h.count('/__l5e'),'leftover root links:',len(re.findall(r'(?:href|src)="/[^/]',h)))
