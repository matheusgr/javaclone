import os
import re


default_order = ['utf-8', 'cp-1252', 'iso8859-15']


def decode_line(line):
    global default_order
    order = default_order
    decoded_line = ''
    try:
        decoded_line = line.strip().decode(order[0])
        default_order = ['utf-8', 'cp-1252', 'iso8859-15']
    except Exception:
        try:
            decoded_line = line.strip().decode(order[1])
            default_order = ['cp-1252', 'iso8859-15', 'utf-8']
        except Exception:
            try:
                decoded_line = line.strip().decode(order[2])
                default_order = ['iso8859-15', 'cp-1252', 'utf-8']
            except Exception:
                try:
                    decoded_line = line.strip().decode('ascii', 'ignore')
                    default_order = ['utf-8', 'cp-1252', 'iso8859-15']
                except Exception:
                    pass
    return decoded_line

def try_mkdir(dirname):
    """ Creates a directory if that directory doesn't exist. """
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


re_stream = re.compile("/\*.*?\*/",re.DOTALL)
re_single = re.compile("//[^\n]*\n")
re_string = re.compile('"[^"]*"', re.DOTALL)
re_spaces = re.compile('\s',re.DOTALL)
re_digits = re.compile('\d',re.DOTALL)
# https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
def remove_comments(string):
    string = re.sub(re_stream, "", string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re_single, "", string) # remove all occurance singleline comments (//COMMENT\n ) from string
    string = re.sub(re_string, "", string) # remove all occurance strings from string
    string = re.sub(re_spaces, "", string) # spaces
    string = re.sub(re_digits, "", string) # digits
    return string


def get_package(code):
    for line in code.splitlines():
        line = decode_line(line)
        if line.startswith('package'):
            package_split = line.split()
            if len(package_split) > 1:
                package = package_split[1].split(';')[0].strip()
                package = package.replace('.', os.sep)
                return package
            break
        elif line.startswith('import') or line.startswith('public') or line.startswith('class') or line.startswith('private'):
            break
    return ''