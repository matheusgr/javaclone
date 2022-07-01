import sys


from skbio import DistanceMatrix
from skbio.tree import nj


distance_matrix = {}
codes_set = set()

fname = sys.argv[1]

for line in open(fname):
    distance, code1, code2 = 1 - float(line.split()[0].strip()), line.split()[1].strip(), line.split()[2].strip()
    distance_vector = distance_matrix.get(code1, {})
    distance_vector[code2] = distance
    distance_matrix[code1] = distance_vector
    distance_vector = distance_matrix.get(code2, {})
    distance_vector[code1] = distance
    distance_matrix[code2] = distance_vector
    codes_set.add(code1)
    codes_set.add(code2)
    distance_matrix[code1][code1] = 0.0
    distance_matrix[code2][code2] = 0.0

distance_function = lambda x, y: distance_matrix[x][y]
label_function = lambda x: x.replace(' ', '')

dm = DistanceMatrix.from_iterable(codes_set, distance_function, label_function)

tree = nj(dm, True)
print(tree.ascii_art())