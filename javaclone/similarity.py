import itertools
import re


def sim(x1, x2):
    sim_ = 0
    dif_ = 0
    i = 0
    j = 0
    lim_x1 = len(x1)
    lim_x2 = len(x2)
    while (i < lim_x1 and j < lim_x2):
        if x1[i] == x2[j]:
            sim_ += 2
            i += 1
            j += 1
        elif x1[i] < x2[j]:
            dif_ += 1
            i += 1
        else:
            dif_ += 1
            j += 1
    dif_ += lim_x1 - i
    dif_ += lim_x2 - j
    return 0 if (dif_ + sim_) == 0 else float(sim_) / (dif_ + sim_)


def sim_pairs(codes):
    result = []
    tmp = []
    for x0, x1 in codes:
        symbols = [x for x in re.findall(r'\w+', x1.lower())]
        tmp.append((x0, symbols))
        tmp[-1][1].sort()
    for x, y in itertools.combinations(tmp, 2):
        result.append((x[0], y[0], sim(x[1], y[1])))
    return result
