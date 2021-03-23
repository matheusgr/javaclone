import os
import sys
import zipfile

from util import decode_line, default_order, try_mkdir, get_package


order = default_order
try_mkdir('work')
work_directory = sys.argv[1] if len(sys.argv) > 1 else "."

for file_ in os.listdir(work_directory):
    if file_.lower().endswith('.zip'):
        try:
            zfile = zipfile.ZipFile(file_)
            student = file_[:-4]  # remove .zip
        except:
            continue
        student_dir = 'work' + os.sep + student + os.sep + 'src' + os.sep
        java_fnames = filter(lambda x: x.lower().endswith('.java'), zfile.namelist())
        for zfile_ in java_fnames:
            zinfo = zfile.getinfo(zfile_)
            zinfo.filename = zinfo.filename.split('/')[-1]
            if not zinfo.filename:
                continue
            raw = zfile.read(zfile_)
            package = get_package(raw)
            try_mkdir(student_dir + package)
            zfile.extract(zinfo, student_dir + package)
