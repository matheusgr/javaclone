import itertools


def sim(x1, x2):
    inter = x1 & x2
    uni = x1 | x2
    total = sum(uni.values())
    common = sum(inter.values())
    return common / total if total > 0 else 0


def sim_pairs(codes):
    result = []
    for (name1, (_, content_counter1)), (name2, (_, content_counter2)) in itertools.combinations(codes, 2):
        result.append((name1, name2, sim(content_counter1, content_counter2)))
    return result
