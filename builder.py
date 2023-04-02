import os,re,shutil


def convert(fr='',t=''):
    static_path = ''
    new_prefix = '{% static \''
    new_postfix = '\' %}'
    inp = ''
    with open(fr, 'r', encoding="utf8") as f:
        inp = f.read()
    inp =inp.replace('static/','')
    html = '{% load static %}{% if MyDebug %}<script>window.baseApiUrl="http://localhost:8000";</script>{% endif %}' + re.sub(rf'(src|href)="({static_path})(.*?)"', fr'\1="{new_prefix}\3{new_postfix}"', inp)

    with open(t,'w+',encoding="utf8") as f:
        f.write(html)


def getPath(dirs):
    t=''
    for f in dirs:
        t = os.path.join(t,f)
    return t

    
convert(fr=getPath(['.','raw','login.html']),t=getPath(['.','auth','templates','auth','login.html']))