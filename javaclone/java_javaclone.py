import os
import sys
import zipfile

from collections import Counter

import utils
import subprocess

def run(dirname, content_counter, content):
    process = subprocess.run(["java", "-jar", "parser.jar", dirname], capture_output=True)
    path_depth = [(-1, "ROOT")]
    for line in process.stdout.splitlines():
        _, depth, name, parent = line.strip().split()
        name = str(name)
        parent = str(parent)
        depth = int(depth)
        cur_node = str(depth) + " " + name + " " + parent
        content_counter[cur_node] += 1
        content.append(cur_node)
        while path_depth[-1][0] >= depth:
            path_depth.pop()
        if path_depth[-1][0] == depth:
            # same level, replace
            path_depth[-1] = (depth, cur_node)
        else:
            path_depth.append((depth, cur_node))

#def run(dirname, content_counter, content):
c = Counter()
content = []
run(sys.argv[1], c, content)
from pprint import pprint
pprint(c)
pprint(content)


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