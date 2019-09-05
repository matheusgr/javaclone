import os
import shutil
import sys


def find_java_files(root):
    flist = [root + os.sep + fname for fname in os.listdir(root)]
    src, test = '', ''
    while len(flist) > 0:
        sub = []
        for fname in flist:
            if os.path.isdir(fname):
                for fname_sub in os.listdir(fname):
                    sub.append(fname + os.sep + fname_sub)
            elif not fname.endswith("package-info.java") and fname.endswith('.java'):
                if 'import org.junit' in open(fname).read():
                    test = fname[len(root) + 1:]
                    test = test.split(os.sep)[0]
                else:
                    src = fname[len(root) + 1:]
                    src = src.split(os.sep)[0]
        flist = sub 
    return (src, test)


def prepare_classpath(src_file, src, test): 
    src_classpath = open(src_file).read()
    src_classpath = src_classpath.replace('%SRC%', src)
    if test and src != test:
        eclipse_cp = '<classpathentry kind="src" path="%SRC%"/>'.replace("%SRC%", test)
        src_classpath = src_classpath.replace('%TEST%', eclipse_cp)
    else:
        src_classpath = src_classpath.replace('%TEST%', '')
    return src_classpath   


def show(project_dir, src, test):
    print("Project dir:", project_dir)
    if src:
        print("- source folder:", src)
    if test:
        print("- test folder:", test)


def prepare_eclipse_files(script_dir, project_dir, project_name, src, test):
    project_eclipse = open(script_dir + os.sep + 'eclipse.project').read().replace('%NAME%', project_name)
    project_classpath = prepare_classpath(script_dir + os.sep + 'eclipse.classpath', src, test)
    project_settings_src = script_dir + os.sep + 'eclipse-settings'
    project_settings_dst = project_dir + os.sep + '.settings' 

    open(project_dir + os.sep + '.project', 'w').write(project_eclipse)
    open(project_dir + os.sep + '.classpath', 'w').write(project_classpath)
    if not os.path.isdir(project_settings_dst):
        shutil.copytree(project_settings_src, project_settings_dst)


def main():
    project_dir = sys.argv[1]
    project_name = os.path.dirname(project_dir + os.sep).split(os.sep)[-1]
    script_dir = os.path.dirname(sys.argv[0])

    src, test = find_java_files(project_dir)
    show(project_dir, src, test)

    prepare_eclipse_files(script_dir, project_dir, project_name, src, test)


if __name__ == "__main__":
    main()
