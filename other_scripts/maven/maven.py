import os
import sys


def process_pkg(fname):
    for line in open(fname, 'rb').readlines():
        if line.strip().startswith(b'package'):
            return line.strip()[len('package '):].split(b';')[0].strip().split(b'.')
    return []


def is_junit_test(fname):
    line = open(fname, 'rb').read().decode('ascii', errors='ignore').strip()
    if 'import org.junit' in line or 'import static org.junit' in line:    
        return True
    return False


def process_java_file(root, fname):
    dirname = fname[len(root) + 1:].split(os.sep)[0:-1]
    pkg = process_pkg(fname)
    while dirname and pkg and dirname != pkg:
        dirname.pop()
        pkg.pop()
    return dirname


def check_dirname(original, new):
    if not original:
        return new
    if original != new:
        print("MISMATCH: ", original, new)
        exit(2)


def find_java_files(root):
    flist = [root + os.sep + fname for fname in os.listdir(root)]
    src, test = '', ''
    while len(flist):
        sub = []
        for fname in flist:
            if os.path.isdir(fname):
                sub.extend([fname + os.sep + fname_sub for fname_sub in os.listdir(fname)])
            elif fname.endswith('.java'):
                dirname = process_java_file(root, fname)
                if (is_junit_test(fname)):
                    test = check_dirname(test, dirname)
                else:
                    src = check_dirname(src, dirname)
        flist = sub
    return (src, test)


def create_src(project_dir):
    if os.path.isdir(project_dir + os.sep + 'src'):
        return ["src"]
    import shutil
    shutil.copytree(project_dir + os.sep, project_dir + os.sep + 'src')
    return ["src"]


def prepare_maven_files(script_dir, project_dir, project_name, src, test):
    if not src:
        src = create_src(project_dir)
    test = '/'.join(test or src)
    src = '/'.join(src)
    print('project_dir: ', project_dir)
    print(' * project_name: ', project_name)
    print(' * src: ', src)
    print(' * test: ', test)
    pom = open(script_dir + os.sep + 'pom.xml.template').read().replace("%NAME%", project_name).replace("%SRC%", src).replace('%TEST%', test or src)
    open(project_dir + os.sep + "pom.xml", 'w').write(pom)


def prepare_project_name(project_name):
    return ''.join(filter(str.isalpha, project_name))


def main():
    project_dir = sys.argv[1]
    project_name = prepare_project_name(os.path.dirname(project_dir + os.sep).split(os.sep)[-1])
    script_dir = os.path.dirname(sys.argv[0])

    src, test = find_java_files(project_dir)

    prepare_maven_files(script_dir, project_dir, project_name, src, test)


if __name__ == "__main__":
    main()
