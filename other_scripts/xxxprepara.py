import os
import zipfile

import chardet

from os.path import dirname, isdir

files = os.listdir('.')
contents = {}


# get student dirname
def get_dirname(fname):
    if '_question_' in fname:
        student = file_[0:fname.find('_question_')]
        if '_' in student:
            fields = student.split('_')
            student = '_'.join(fields[1:]) + '_' + fields[0]
    else:
        student = fname.split("_")[0]
    return student


# Remove unecessary parent dirs
# returns (common directory, list of files without common dir)
def detect_unecessary_parent_dirs(fnames):
    ref = fnames[0]
    common = ''
    found = False
    for i, c in enumerate(ref):
        for fname in fnames:
            if fname[i] != c:
                found = True
                break
        if found:
            break
        common += c
    result = []
    for fname in fnames:
        result.append(fname[len(common):])
    return (common, result)

os.mkdir('work')

for file_ in files:
    if file_.lower().endswith('.zip'):
        try:
            zfile = zipfile.ZipFile(file_)
        except:
            continue
        student = get_dirname(file_)
        student_dir = 'work' + os.sep + student
        os.mkdir(student_dir)
        student_files = []
        for zfile_ in zfile.namelist():
            if 'RemoteSystemsTempFiles' in zfile_ or '.metadata' in zfile_:
                continue
            student_files.append(zfile_)
        common, _ = detect_unecessary_parent_dirs(student_files)
        for zfile_ in student_files:
            zinfo = zfile.getinfo(zfile_)
            print(zinfo.filename)
            zinfo.filename = zinfo.filename[len(common):]
            if not zinfo.filename:
                continue
            zfile.extract(zinfo, student_dir)
