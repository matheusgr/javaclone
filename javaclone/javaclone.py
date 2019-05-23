import itertools
import os
import sys
import zipfile

import javalang

import similarity
import utils


def error(e):
    print(e, file=sys.stderr)


def process_java_code(code):
    tree = javalang.parse.parse(code)
    code = ''
    for path, node in tree:
        if len(path) > 0:
            t = path[-1]
            while type(t) == list:
                t = t[-1]
            parent_type = type(t).__name__
        else:
            parent_type = ''
        node_name = parent_type + type(node).__name__
        code += ("a" * len(path)) + str(node_name) + " "
    return code    


def process_content(raw):
    code = raw.decode('ascii', 'ignore')
    try:
        return process_java_code(code)
    except:
        return utils.remove_comments(code)


def process_zip(zip_file):
    try:
        zfile = zipfile.ZipFile(zip_file)
    except zipfile.BadZipFile as e:
        error(e)
    content = ''
    for zfile_ in zfile.namelist():
        if not zfile_.lower().endswith('.java'):
            continue
        raw = zfile.read(zfile_)
        content += process_content(raw) + " "
    return content
        


def process(directory='.'):
    files = os.listdir(directory)
    contents = {}
    for file_ in files:
        if file_.lower().endswith('.zip'):
            contents[file_] = process_zip(file_)
    return contents
