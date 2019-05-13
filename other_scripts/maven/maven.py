import os
import shutil
import sys


def find_java_files(root):
    flist = [root + os.sep + fname for fname in os.listdir(root)]
    src, test, pkg = '', '', ''
    pkgs = []
    while len(flist) > 0:
        sub = []
        for fname in flist:
            if os.path.isdir(fname):
                for fname_sub in os.listdir(fname):
                    sub.append(fname + os.sep + fname_sub)
            elif fname.endswith('.java'):
                if 'import org.junit' in open(fname).read():
                    test = fname[len(root) + 1:]
                    test = test.split(os.sep)[0]
                    for line in open(fname).readlines():
                        if line.strip().startswith('package'):
                            pkgs.append(line.strip()[len('package '):].split(';')[0].strip())
                else:
                    src = fname[len(root) + 1:]
                    src = src.split(os.sep)[0]
        pkgs.sort()
        if pkgs:
            pkg = pkgs[0].split('.')[0]
        flist = sub 
    return (src, test, pkg)


def prepare_maven_files(script_dir, project_dir, project_name, src, test, pkg):
    pom = open(script_dir + os.sep + 'pom.xml').read().replace("%NAME%", project_name).replace("%SRC%", src).replace('%TEST%', test or src).replace("%PKG%", pkg)
    open(project_dir + os.sep + "pom.xml", 'w').write(pom)


def main():
    project_dir = sys.argv[1]
    project_name = os.path.dirname(project_dir + os.sep).split(os.sep)[-1]
    script_dir = os.path.dirname(sys.argv[0])

    src, test, pkg = find_java_files(project_dir)

    prepare_maven_files(script_dir, project_dir, project_name, src, test, pkg)


if __name__ == "__main__":
    main()
