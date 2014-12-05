from collections import defaultdict
from scipy.sparse import csr_matrix
import random
import networkx, pickle

partition = pickle.load(open('final_partition_subgraphs.pickle'))

def getSimilarUsers(primary, sub, N):
    featuresPrimary = featureVectors[primary][sub]
    similarityScores = set()
    for other in subToUser[sub]:
        if primary != other:
            featuresOther = featureVectors[other][sub]
            numerator = dot(featuresPrimary, featuresOther)
            denominator = norm(featuresPrimary) * norm(featuresOther)
            if denominator:
                score = float(numerator) / denominator
            else:
                score = 0.
            similarityScores.add((score, other))
    sortedScores = sorted(similarityScores, key = lambda tup: tup[0], reverse=True)
    topNScores = []
    current = 0
    for (score, user) in sortedScores:
        topNScores.append(user)
        current += 1
        if (current == N):
            break
    return topNScores

def testUser(user, sub):
    similarUsers = getSimilarUsers(user, sub, 100)
    cluster = 0
    for clusterID in range(len(partition)):
        subs = networkx.nodes(partition[clusterID])
        if sub in subs:
            cluster = clusterID

    commonSubs = defaultdict(int)
    for user in similarUsers:
        for sub in featureVectors[user]:
            if sub in networkx.nodes(partition[cluster]):
                commonSubs[sub] += 1
    sortedCommonSubs = sorted(commonSubs.items(), key = lambda x: x[1], reverse=True)
    topNRecs = []
    for x in sortedCommonSubs:
        if x[1] > 10:
            topNRecs.append(x[0])
    return topNRecs

successes = 0
total = 0
for i in range(0, 100):
    user = powerUsers[random.randint(0, 890)]
    sub = random.choice(featureVectors[user].keys())
    recommendedSubs = testUser(user, sub)
    for r in recommendedSubs:
        total += 1
        if r in featureVectors[user]:
            successes += 1
print successes * 1.0 / total
