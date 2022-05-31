import os
import sys
import zipfile

from collections import Counter

import javalang

import utils


def error(e):
    print(e, file=sys.stderr)

CONFIG = {'node_depth' : lambda path: 'P' * len(path),
            'parent': True}


def process_java_code(code, content, content_counter):
    tree = javalang.parse.parse(code)
    path_depth = [(-1, "ROOT")]
    for path, node in tree:
        # ast node depth create different nodes
        cur_node = (CONFIG['node_depth'](path)) + node.__class__.__name__  
        # cur_node is closer to root than actual parent on list:
        while path_depth[-1][0] >= len(path):
            path_depth.pop()
        # append current node with parent:
        processed_node = path_depth[-1][1] + cur_node if CONFIG["parent"] else cur_node
        content_counter[processed_node] += 1
        content.append(processed_node)
        if path_depth[-1][0] == len(path):
            # same level, replace
            path_depth[-1] = (len(path), cur_node)
        else:
            # new level, append
            path_depth.append((len(path), cur_node))


def process_content(raw, content, content_counter):
    code = utils.decode_line(raw)
    try:
        process_java_code(code, content, content_counter)
        return True
    except Exception:
        # Ignore content. Alternative: use text extracted from code:
        #  comments = utils.remove_comments(code).split()
        #  content.extend(comments)
        #  content_counter.update(comments)
        pass
    return False


def process_zip(zip_file):
    content = []
    content_counter = Counter()
    try:
        zfile = zipfile.ZipFile(zip_file)
    except zipfile.BadZipFile:
        error("Badzipfile " + zip_file)
        return content, content_counter
    for zfile_ in zfile.namelist():
        if not zfile_.lower().endswith('.java') or \
                    zfile_.lower().endswith('module-info.java') or \
                    zfile_.lower().endswith('package-info.java'):
            continue
        raw = zfile.read(zfile_)
        if b'@Test' in raw:
            continue
        if not process_content(raw, content, content_counter):
            sys.stderr.write("Error parsing file in " + zip_file)
    return content, content_counter
        


def process(directory='.'):
    files = os.listdir(directory)
    contents = {}
    for file_ in files:
        if file_.lower().endswith('.zip'):
            contents[file_] = process_zip(directory + os.sep + file_)
    return contents
