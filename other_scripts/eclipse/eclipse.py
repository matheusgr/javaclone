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
                if os.path.basename(fname) == 'src':
                    src = fname[len(root) + 1:]
                if os.path.basename(fname).startswith('test'):
                    test = fname[len(root) + 1:]
                for fname_sub in os.listdir(fname):
                    sub.append(fname + os.sep + fname_sub)
            elif not fname.endswith("package-info.java") and fname.endswith('.java'):
                if b'import org.junit' in open(fname, 'rb').read():
                    test = fname[len(root) + 1:]
                    test = test.split(os.sep)[0]
                else:
                    if not src:
                        src = fname[len(root) + 1:]
                        src = src.split(os.sep)[0]
                        if os.path.isfile(root + os.sep + src):
                            src = '.'
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


def remove_hidden_files(cur_dir):
    for fname in os.listdir(cur_dir):
        c_file = cur_dir + os.sep + fname
        if fname.startswith('.'):
            if os.path.isdir(c_file):
                shutil.rmtree(c_file)
            else:
                os.remove(c_file)
        else:
            if os.path.isdir(c_file):
                remove_hidden_files(c_file)


def main():
    if sys.argv[1] == '-s':
        for project_dir in os.listdir(sys.argv[2]):
            if os.path.isdir(project_dir):
                remove_hidden_files(project_dir)
                project_name = os.path.dirname(project_dir + os.sep).split(os.sep)[-1]
                script_dir = os.path.dirname(sys.argv[0])

                src, test = find_java_files(project_dir)
                show(project_dir, src, test)

                prepare_eclipse_files(script_dir, project_dir, project_name, src, test)
        return
                
    project_dir = sys.argv[1]
    project_name = os.path.dirname(project_dir + os.sep).split(os.sep)[-1]
    script_dir = os.path.dirname(sys.argv[0])

    src, test = find_java_files(project_dir)
    show(project_dir, src, test)

    prepare_eclipse_files(script_dir, project_dir, project_name, src, test)


if __name__ == "__main__":
    main()
