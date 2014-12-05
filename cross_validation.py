from collections import defaultdict
from scipy.sparse import csr_matrix
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
    similarUsers = getSimilarUsers(user, sub, 1000)
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
    print sortedCommonSubs
    for x in sortedCommonSubs:
        print x[0] in featureVectors[user]

testUser("17d2a48714c3cbee0257334a6f7a0d7c", "877afdc80d3fe9c0ce9b6d75453531ce")
