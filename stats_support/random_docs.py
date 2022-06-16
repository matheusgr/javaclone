import bisect
from collections import Counter
import random
import sys

from scipy.stats import norm

sys.path.append('../javaclone')
import similarity

freqs = list(map(int, open('results/freq.txt').readlines()))

values = [freqs[0]]
for index, freq in enumerate(freqs[1:]):
    values.append(values[-1] + freq)

max_value = values[-1]

docs_size = 99

r = norm.rvs(loc=850.4117647058823, scale=241.92343436898753, size=docs_size)
docs = []
for length in r:
    doc = []
    for x in range(int(length)):
        doc.append(bisect.bisect_left(values, random.randint(0, max_value)))
    docs.append(doc)

docs_counter = []
i = 0
for doc in docs:
    print('counting...')
    docs_counter.append((i, ('', Counter(doc))))
    i += 1

print("similarity...")

pairs = similarity.sim_pairs(docs_counter)
sim_per_doc = dict([(x, 0) for x in range(docs_size)])

for pair in sorted(pairs, key=lambda x: x[2]):
    sim_per_doc[pair[0]] = max(sim_per_doc[pair[0]], pair[2])
    sim_per_doc[pair[1]] = max(sim_per_doc[pair[1]], pair[2])
    print(pair)

for v in sorted(list(set(sim_per_doc.values()))):
    # get max unique similarity
    print(v)