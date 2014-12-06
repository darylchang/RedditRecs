from collections import defaultdict
from scipy.sparse import csr_matrix
import random
import networkx, pickle

partition = pickle.load(open('final_partition_subgraphs.pickle'))
similarityScores = pickle.load(open('similarity_scores.dump', 'r'))

def getSimilarSubs(primarySub, N):
    cluster = -1
    for clusterID in range(len(partition)):
        subs = networkx.nodes(partition[clusterID])
        if primarySub in subs:
            cluster = clusterID
    if cluster == -1:
        print "error"

    sortedScores = sorted(similarityScores[cluster][primarySub].items(), key = lambda x: x[1], reverse=True)
    topNScores = []
    current = 0
    for (sub, score) in sortedScores:
        topNScores.append(sub)
        current += 1
        if (current == N):
            break
    return topNScores

successes = 0
total = 0
for i in range(0, 100):
    user = powerUsers[random.randint(0, 890)]
    sub = random.choice(featureVectors[user].keys())
    recommendedSubs = getSimilarSubs(sub, 3)
    for r in recommendedSubs:
        total += 1
        if r in featureVectors[user]:
            successes += 1
print successes * 1.0 / total
