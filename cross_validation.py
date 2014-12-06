from collections import defaultdict
from matplotlib import pyplot
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

def testUser(user, sub, similarUsers, percentage):
    similarUsers = getSimilarUsers(user, sub, numUsers)
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

    numRecommended = 0
    for x in sortedCommonSubs:
        if x[1] > percentage * len(similarUsers):
            topNRecs.append(x[0])
            numRecommended += 1

        if numRecommended == 3:
            break

    return topNRecs

powerUsers = pickle.load(open('power_users.dump'))
numUsersRange = [100, 1000, 2000, 3000, 4000, 5000]
precision = defaultdict(list)

for i in range(0, 100):
    print i
    user = powerUsers[random.randint(0, 890)]
    sub = random.choice(featureVectors[user].keys())
    similarUsers = getSimilarUsers(user, sub, 5000)

    for numUsers in numUsersRange:
        similarUsersSubset = similarUsers[:numUsers]
        recommendedSubs = testUser(user, sub, similarUsersSubset, 0.1)

        for r in recommendedSubs:
            total += 1
            if r in featureVectors[user]:
                successes += 1
    if total:       
        precision[numUsers].append(successes * 1.0 / total)

y = [sum(precision[numUsers].values())/len(precision[numUsers].values()) for numUsers in numUserRange]

pyplot.plot(numUserRange, y)
pyplot.show()