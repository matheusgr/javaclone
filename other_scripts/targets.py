import os


files = os.listdir('.')
contents = {}
res = ''
for file_ in sorted(files):
    if os.path.isdir(file_) and os.path.isdir(file_ + os.sep + 'target'):
            res += '<a href=' + file_ + os.sep + 'target' + os.sep + 'site' + os.sep + 'project-reports.html>' + file_ + '</a><br>'
            res += '<img src="' + file_ + os.sep + 'target' + os.sep + 'plantuml' + os.sep + 'Maven Quick Start Archetype.urm.png' +'"></img><br><br>'

open('res.html', 'w').write(res)
