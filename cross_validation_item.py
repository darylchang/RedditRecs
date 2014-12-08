from collections import defaultdict
from scipy.sparse import csr_matrix
import random
import networkx, pickle

#partition = pickle.load(open('data/final_partition_subgraphs.pickle'))
subToCluster = pickle.load(open('data/sub_to_cluster_id.dump'))
similarityScores = pickle.load(open('data/similarity_scores.dump', 'r'))

def getSimilarSubs(primarySub, N):
    cluster = subToCluster[primarySub]
    sortedScores = sorted(similarityScores[cluster][primarySub].items(), key = lambda x: x[1], reverse=True)
    topNScores = []
    current = 0
    for (sub, score) in sortedScores:
        if sub != primarySub:
            topNScores.append(sub)
            current += 1
            if (current == N):
                break
    return topNScores

successes = 0
total = 0
for i in range(0, 100):
    user = powerUsers[random.randint(0, 890)]
    sub = random.choice([x for x in featureVectors[user].keys() if x in subToCluster])
    recommendedSubs = getSimilarSubs(sub, 3)
    for r in recommendedSubs:
        total += 1
        if r in featureVectors[user]:
            successes += 1
print successes * 1.0 / total
