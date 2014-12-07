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
numUsersRange = [100, 1000, 2000, 3000, 4000, 5000, 10000]
precision = defaultdict(list)

for i in range(0, 100):
    print i
    user = powerUsers[random.randint(0, 890)]
    sub = random.choice(featureVectors[user].keys())
    similarUsers = getSimilarUsers(user, sub, 10000)

    for numUsers in numUsersRange:
        total, successes = 0., 0.
        similarUsersSubset = similarUsers[:numUsers]
        recommendedSubs = testUser(user, sub, similarUsersSubset, 0.1)

        for r in recommendedSubs:
            total += 1
            if r in featureVectors[user]:
                successes += 1
        if total:       
            precision[numUsers].append(successes * 1.0 / total)

y = [sum(precision[numUsers])/len(precision[numUsers]) for numUsers in numUsersRange]

pyplot.plot(numUsersRange, y)
pyplot.title('Precision of Recommendations vs. Number of Similar Users')
pyplot.xlabel('Number of Similar Users')
pyplot.ylabel('Precision of recommendations')
pyplot.show()

# powerUsers = pickle.load(open('power_users.dump'))
# percentages =[0.02*x for x in range(1,10)]
# precision = defaultdict(list)

# for i in range(0, 100):
#     print i
#     user = powerUsers[random.randint(0, 890)]
#     sub = random.choice(featureVectors[user].keys())
#     similarUsers = getSimilarUsers(user, sub, 100)

#     for percentage in percentages:
#         total, successes = 0., 0.
#         recommendedSubs = testUser(user, sub, similarUsers, percentage)

#         for r in recommendedSubs:
#             total += 1
#             if r in featureVectors[user]:
#                 successes += 1
#         if total:       
#             precision[percentage].append(successes * 1.0 / total)

# y = [sum(precision[percentage])/len(precision[percentage]) for percentage in percentages]

# pyplot.plot(percentages, y)
# pyplot.title('Precision of Recommendations vs. Recommendation Threshold')
# pyplot.xlabel('Recommendation threshold for percentage of users interested')
# pyplot.ylabel('Precision of recommendations')
# pyplot.show()