import os
import re


default_order = ['utf-8', 'cp-1252', 'iso8859-15']


def decode_line(line, order):
    try:
        return (line.strip().decode(order[0]), ['utf-8', 'cp-1252', 'iso8859-15'])
    except:
        try:
            return line.strip().decode(order[1], ['cp-1252', 'iso8859-15', 'utf-8'])
        except:
            try:
                return (line.strip().decode(order[2]), ['iso8859-15', 'cp-1252', 'utf-8'])
            except:
                return ('', order)


def try_mkdir(dirname):
    """ Creates a directory if that directory doesn't exist. """
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def get_package(code):
    for line in code.splitlines():
        line, order = decode_line(line, order)
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