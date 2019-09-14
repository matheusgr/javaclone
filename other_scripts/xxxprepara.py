import os
import zipfile


files = os.listdir('.')
contents = {}


def process_student_name(name):
    fields = name.split('_')
    if len(fields) > 1:
        name = fields[1:] + [fields[0]]
        return '_'.join(name)
    return name


def try_mkdir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)


def finddir(namelist):
    candidates = []
    java_files = []
    for fname in namelist:
        if 'RemoteSystemsTempFiles' in fname or '.metadata' in fname:
            continue
        if '.project' in fname or '.iml' in fname:
            candidates.append(os.path.dirname(fname))
        if '.java' in fname:
            java_files.append(fname)
    if len(candidates) == 1:
        return candidates[0]
    guess = os.path.dirname(java_files[0])
    for java_file in java_files[1:]:
        dirname = os.path.dirname(java_file)
        current = ''
        for x, y in zip(dirname, guess):
            if x == y:
                current += x
            else:
                break
        guess = current
    return guess

try_mkdir('work')

for file_ in files:
    if file_.lower().endswith('.zip'):
        try:
            zfile = zipfile.ZipFile(file_)
            if '_question_' in file_:
                student = file_[0:file_.find('_question_')]
            else:
                student = file_.split("_")[0]
            student = process_student_name(student)
        except Exception as e:
            print(e)
            continue
        content = ''
        ref_dir = finddir(zfile.namelist())
        student_dir = 'work' + os.sep + student
        try_mkdir(student_dir)
        student_files = []
        for zfile_ in zfile.namelist():
            if 'RemoteSystemsTempFiles' in zfile_ or '.metadata' in zfile_:
                continue
            if zfile_.startswith(ref_dir):
                student_files.append(zfile_)
                continue
        for zfile_ in student_files:
            zinfo = zfile.getinfo(zfile_)
            zinfo.filename = zinfo.filename[len(ref_dir):]
            if not zinfo.filename:
                continue
            zfile.extract(zinfo, student_dir)
        contents[file_] = content
