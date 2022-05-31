import argparse

import javaclone
import similarity


def print_terms(directory):
    contents = javaclone.process(directory)
    terms = {}
    total_terms_per_program = []
    for _, (_, content_counter) in contents.items():
        size = 0
        for prog_term, prog_count in content_counter.items():
            terms[prog_term] = terms.get(prog_term, 0) + prog_count
            size += prog_count
        total_terms_per_program.append(size)
    total_terms_per_program.sort()
    print("Number of terms per program:")
    print('\n'.join([str(x) for x in total_terms_per_program]))
    print("Terms and frequency:")
    for term, freq in sorted(terms.items(), key=lambda x: x[1]):
        print(term, freq)


def print_sims(directory):
    contents = javaclone.process(directory)
    items = contents.items()
    simi = similarity.sim_pairs(items)
    simi.sort(key=lambda x: x[2])
    for x, y, z in simi:
        print(str(z) + " " + x[:40] + " " + y[:40])


def main():
    parser = argparse.ArgumentParser(description='Compare java code.')
    parser.add_argument('directory', metavar='dir', type=str, nargs="?", default='.',
                        help='directory with zip files with java codes to be compared')
    parser.add_argument('--terms', action="store_true",
                        help='print terms of evaluated java files')

    args = parser.parse_args()

    if args.terms:
        print_terms(args.directory)
    else:
        print_sims(args.directory)

if __name__ == "__main__":
    main()
