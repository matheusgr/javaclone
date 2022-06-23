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


def find_java_files(root):
    flist = [root + os.sep + fname for fname in os.listdir(root)]
    src, test = '', ''
    while len(flist) > 0:
        sub = []
        for fname in flist:
            if os.path.isdir(fname):
                for fname_sub in os.listdir(fname):
                    sub.append(fname + os.sep + fname_sub)
            elif fname.endswith('.java'):
                dirname = process_java_file(root, fname)
                if (is_junit_test(fname)):
                    if not test:
                        test = dirname
                    if test and test != dirname:
                        print("MISMATCH: ", test, dirname)
                        exit(2)
                else:
                    if not src:
                        src = dirname
                    if src and src != dirname:
                        print("MISMATCH: ", src, dirname)
                        exit(2)
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
