import os
import zipfile

import chardet

import fileinput


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


def simplify(fnames):
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


def project(fname, pname):
    once = False
    project_file = open(fname, 'rb')
    project = project_file.readlines()
    project_file.close()
    project_file = open(fname, 'w')
    for line in project:
        if not once and line.strip().startswith(b"<name>"):
            project_file.write("<name>" + pname + "</name>\n")
            once = True
        else:
            project_file.write(line.decode('utf-8'))
    project_file.close()


def finddir(namelist):
    candidates = []
    java_files = []
    for fname in namelist:
        if 'RemoteSystemsTempFiles' in fname or '.metadata' in fname:
            continue
        if '.project' in fname:
            candidates.append([fname[:-(1 + len('.project'))], 0])
        if '.iml' in fname:
            candidates.append([fname[:-(1 + len('.iml'))], 0])
        if '.java' in fname:
            java_files.append(fname)
    if len(candidates) == 1:
        return candidates[0][0]
    if not candidates:
        return namelist[0]
    for candidate in candidates:
        for java_file in java_files:
            if candidate[0] in java_file:
                candidate[1] += 1
    candidates.sort(key=lambda x: x[1])
    return candidates[-1][0]

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
            else:
                continue
            if zfile_.lower().endswith('.java') and not zfile_.lower().endswith('test.java'):
                raw = zfile.read(zfile_)
                encoding = chardet.detect(raw)['encoding']
                code = raw.decode(encoding)
                try:
                    tree = javalang.parse.parse(code)
                    code = ''
                    for path, node in tree:
                        code += ("a" * len(path)) + str(node) + " "
                    content += code
                except:
                    code = raw.decode(encoding)
                    content += remove_comments(code)
        common, _ = simplify(student_files)
        for zfile_ in student_files:
            zinfo = zfile.getinfo(zfile_)
            zinfo.filename = zinfo.filename[len(common):]
            if not zinfo.filename:
                continue
            zfile.extract(zinfo, student_dir)
            if zinfo.filename.endswith('.project'):
                project(student_dir + os.sep + zinfo.filename, student)
        contents[file_] = content
