from collections import defaultdict
from scipy.sparse import csr_matrix
import networkx, pickle

def dot(userA, userB):
	result = 0.0
	for subpost in userA:
		if subpost in userB:
			result += 1
	return result

def norm(user):
	return sum([user[x]**2 for x in user])**0.5

featureVectors = defaultdict(lambda: defaultdict(dict))
subToUser = defaultdict(set)

for line in open('users_sorted.dump'):
    user, link, sub, vote = line.split()
    subToUser[sub].add(user)
    if link not in featureVectors[user][sub]:
		featureVectors[user][sub][link] = 1
    else:
		featureVectors[user][sub][link] += 1

print "finished creating feature vectors"

POWER_USER_THRESHOLD = 100
powerUsers = []
for user in featureVectors:
    if len(featureVectors[user]) > POWER_USER_THRESHOLD:
        powerUsers.append(user)

print "finished identifying power users"
