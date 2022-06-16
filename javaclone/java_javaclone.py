import os
import sys

from collections import Counter

import subprocess

def process_content(zip_file, content, content_counter):
    process = subprocess.run(["java", "-jar", "parser.jar", zip_file], capture_output=True)
    path_depth = [(-1, "ROOT")]
    if process.returncode != 0:
        return False
    for line in process.stdout.splitlines():
        if len(line.strip().split(b";")) != 4:
            return False
        _, depth, name, parent = line.strip().split(b";")
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
    return True


def process_zip(zip_file):
    content = []
    content_counter = Counter()
    if not process_content(zip_file, content, content_counter):
        sys.stderr.write("Error parsing file in " + zip_file + "\n")
    return content, content_counter


def process(directory='.'):
    contents = {}
    if os.path.isfile(directory):
        contents[directory] = process_zip(directory)
        return contents
    files = os.listdir(directory)
    for file_ in files:
        if file_.lower().endswith('.zip'):
            contents[file_] = process_zip(directory + os.sep + file_)
    return contents

if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):
        print(process(sys.argv[1]))
    else:
        print(process_zip(sys.argv[1]))