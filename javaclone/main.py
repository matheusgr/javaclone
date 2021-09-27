import sys

import javaclone
import similarity


def print_terms():
    contents = javaclone.process()
    from pprint import pprint
    terms = {}
    sizes = []
    for filename, (content, content_counter) in contents.items():
        size = 0
        for prog_term, prog_count in content_counter.items():
            terms[prog_term] = terms.get(prog_term, 0) + prog_count
            size += prog_count
        sizes.append(size)
    sizes.sort()
    print('\n'.join([str(x) for x in sizes]))
    print(sizes[int(len(sizes) / 2)])
    l_terms = list(terms.items())
    l_terms.sort(key=lambda x: x[1])
    for l, t in l_terms:
        print(l, t)


def print_sims():
    contents = javaclone.process()
    items = contents.items()
    simi = similarity.sim_pairs(items)
    simi.sort(key=lambda x: x[2])
    for x, y, z in simi:
        print(x[:40] + ' ' + y[:40] + ' ' + str(z))


def main():
    if len(sys.argv) > 1:
        print_terms()
    else:
        print_sims()

if __name__ == "__main__":
    main()
