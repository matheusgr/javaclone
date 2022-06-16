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
                line = open(fname, 'rb').read().decode('ascii', errors='ignore').strip()
                if 'import org.junit' in line or 'import static org.junit' in line:
                    test = fname[len(root) + 1:]
                    test = test.split(os.sep)[0]
                else:
                    src = fname[len(root) + 1:]
                    src = src.split(os.sep)[0]
                    for line in open(fname, 'rb').readlines():
                        if line.strip().startswith(b'package'):
                            pkgs.append(line.strip()[len('package '):].split(b';')[0].strip())
        pkgs.sort()
        if pkgs:
            pkg = pkgs[0].split(b'.')[0].decode('utf-8')
        flist = sub 
    return (src, test, pkg)


def prepare_maven_files(script_dir, project_dir, project_name, src, test, pkg):
    pom = open(script_dir + os.sep + 'pom.xml.template').read().replace("%NAME%", project_name).replace("%SRC%", src).replace('%TEST%', test or src).replace("%PKG%", pkg)
    open(project_dir + os.sep + "pom.xml", 'w').write(pom)


def main():
    project_dir = sys.argv[1]
    project_name = os.path.dirname(project_dir + os.sep).split(os.sep)[-1]
    script_dir = os.path.dirname(sys.argv[0])

    src, test, pkg = find_java_files(project_dir)

    prepare_maven_files(script_dir, project_dir, project_name, src, test, pkg)


if __name__ == "__main__":
    main()
