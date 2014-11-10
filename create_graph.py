import snap
from random import randint

nodes = open('subs_unique.dump', 'r')
keys = []
for sub in nodes: keys.append(sub.rstrip('\n'))

pairs = []
for k in keys: pairs.append((k, 0))

dict_pairs = []
for k in keys:
    temp = dict(pairs)
    dict_pairs.append((k, temp))

edge_map = dict(dict_pairs)

users = open('users_sorted.dump', 'r')
current_subs = set()
current_user = '0'
for line in users:
    l = line.split('\t')
    if (current_user != '0' and l[0] != current_user):
        for s1 in current_subs:
            for s2 in current_subs:
                if (s1 != s2):
                    edge_map[s1][s2] += 1
                    edge_map[s2][s1] += 1
        current_subs = set()
    current_user = l[0]
    current_subs.add(l[2])

for s1 in keys:
    total = 0
    for s2 in keys:
        total += edge_map[s1][s2]
    for s2 in keys:
        edge_map[s1][s2] /= total

edge_map_new = edge_map
THRESHOLD = 0.005
for s1 in keys:
    for s2 in keys:
        if (edge_map[s1][s2] < THRESHOLD and edge_map[s2][s1] < THRESHOLD):
            edge_map_new[s1][s2] = 0;
            edge_map_new[s2][s1] = 0;
        else:
            edge_map_new[s1][s2] = 1;
            edge_map_new[s2][s1] = 1;
