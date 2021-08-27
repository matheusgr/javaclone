import itertools
import os
import sys
import zipfile

from collections import Counter

import javalang

import similarity
import utils


def error(e):
    print(e, file=sys.stderr)


def process_java_code(code, content, content_counter):
    tree = javalang.parse.parse(code)
    path_depth = [(-1, "ROOT")]
    for path, node in tree:
        # ast node depth create different nodes
        cur_node = ('P' * len(path)) + node.__class__.__name__  
        # cur_node is closer to root than actual parent on list:
        while path_depth[-1][0] >= len(path):
            path_depth.pop()
        # append current node with parent:
        content_counter[path_depth[-1][1] + cur_node] += 1
        content.append(path_depth[-1][1] + cur_node)  
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
    except Exception as e:
        comments = utils.remove_comments(code).split()
        content.extend(comments)
        content_counter.update(comments)


def process_zip(zip_file):
    content = []
    content_counter = Counter()
    try:
        zfile = zipfile.ZipFile(zip_file)
    except zipfile.BadZipFile as e:
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
        process_content(raw, content, content_counter)
    return content, content_counter
        


def process(directory='.'):
    files = os.listdir(directory)
    contents = {}
    for file_ in files:
        if file_.lower().endswith('.zip'):
            contents[file_] = process_zip(file_)
    return contents
