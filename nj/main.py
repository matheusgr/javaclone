from pprint import pprint
import numpy as np

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

import sys

f_ = sys.argv[1]

connections = []
pairs = {}

for l in open(f_, 'r', encoding='utf-8').readlines():
    conn = l.split()
    pairs[conn[1]] = pairs.get(conn[1], {})
    pairs[conn[2]] = pairs.get(conn[2], {})
    pairs[conn[1]][conn[2]] = float(conn[0])
    pairs[conn[2]][conn[1]] = float(conn[0])

labels = list(pairs.keys())
labels.sort()

pprint(list(enumerate(labels)))
result = []

for l1 in labels:
    result.append([])
    for l2 in labels:
        if l1 == l2:
            result[-1].append(0.0)
        else:
            # Use dissimilarity:
            result[-1].append(1 - pairs[l1][l2])

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)



# setting distance_threshold=0 ensures we compute the full tree.
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None, affinity='precomputed', linkage='average')
X = result
model = model.fit(X)
plt.title('Hierarchical Clustering Dendrogram')
# plot the top three levels of the dendrogram
#plot_dendrogram(model, truncate_mode='level', p=3)
plot_dendrogram(model)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()
