from collections import defaultdict
from matplotlib import pyplot
from scipy.sparse import csr_matrix
import random
import networkx, pickle

partition = pickle.load(open('data/final_partition_subgraphs.pickle'))
subToCluster = pickle.load(open('data/sub_to_cluster_id.dump'))
#featureVectors = pickle.load(open('data/feature_vectors.dump'))
#subToUser = pickle.load(open('data/sub_to_user.dump'))

def getSimilarUsers(primary, sub, N, activityThreshold=0.):
    featuresPrimary = featureVectors[primary][sub]
    similarityScores = set()
    clusterID = subToCluster[sub]
    communitySubs = [s for s, c in subToCluster.items() if c == clusterID]

    for other in subToUser[sub]:
        if primary != other:
            if sub not in featureVectors[other]:
                print other, sub, norm(featureVectors[other][sub]),'\n\n\n\n'
            featuresOther = featureVectors[other][sub]
            numerator = dot(featuresPrimary, featuresOther)
            denominator = norm(featuresPrimary) * norm(featuresOther)
            score = float(numerator) / denominator if denominator else 0.
        
            if sum([norm(links) for sub, links in featureVectors[other].items() if sub in communitySubs]) > activityThreshold:
                similarityScores.add((score, other))

    sortedScores = sorted(similarityScores, key = lambda tup: tup[0], reverse=True)
    topNScores = []
    current = 0
    for (score, user) in sortedScores:
        topNScores.append((score, user))
        current += 1
        if (current == N):
            break
    return topNScores

def getTopRecs(user, activeSub, similarUsers, percentage):
    commonSubs = defaultdict(int)
    for similarityScore, similarUser in similarUsers:
        for sub in featureVectors[similarUser]:
            if sub in subToCluster and subToCluster[sub] == subToCluster[activeSub] and sub != activeSub:
                #commonSubs[sub] += 1
                commonSubs[sub] += similarityScore
    sortedCommonSubs = sorted(commonSubs.items(), key = lambda x: x[1], reverse=True)
    return sortedCommonSubs[:3]

    # topNRecs = []

    # numRecommended = 0
    # for x in sortedCommonSubs:
    #     if x[1] > 1:
    #         topNRecs.append(x[0])
    #         numRecommended += 1

    #     if numRecommended == 3:
    #         break

    # return topNRecs

powerUsers = pickle.load(open('data/power_users.dump'))
numUsersRange = [2, 3, 4, 5, 10, 50, 100, 500, 1000]
precision = defaultdict(list)

for i in range(0, 10):
    print i
    user = random.choice(powerUsers)
    sub = random.choice([sub for sub in featureVectors[user].keys() if sub in subToCluster]) 
    similarUsers = getSimilarUsers(user, sub, max(numUsersRange))

    for numUsers in numUsersRange:
        
        similarUsersSubset = similarUsers[:numUsers]
        total, successes = 0., 0.
        recommendedSubs = getTopRecs(user, sub, similarUsersSubset, 0.1)

        if recommendedSubs:
            for r in recommendedSubs:
                total += 1
                if r in featureVectors[user]:
                    successes += 1
            if total:       
                precision[numUsers].append(successes * 1.0 / total)
        else:
            precision[numUsers].append(0.)

y = [sum(precision[numUsers])/len(precision[numUsers]) for numUsers in numUsersRange]
print y

pyplot.plot(numUsersRange, y)
pyplot.title('Precision of Recommendations vs. Activity Threshold')
pyplot.xlabel('Activity threshold for similar users')
pyplot.ylabel('Precision of recommendations')
pyplot.show()

# pyplot.plot(numUsersRange, y)
# pyplot.title('Precision of Recommendations vs. Number of Similar Users')
# pyplot.xlabel('Number of Similar Users')
# pyplot.ylabel('Precision of recommendations')
# pyplot.show()

# powerUsers = pickle.load(open('data/power_users.dump'))
# percentages =[0.02*x for x in range(1,10)]
# precision = defaultdict(list)

# for i in range(0, 10):
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

# powerUsers = pickle.load(open('data/power_users.dump'))
# activityThresholds = [0]#, 10, 20, 30, 50, 100]
# precision = defaultdict(list)

# for i in range(0, 10):
#     print i
#     user = random.choice(powerUsers)
#     sub = random.choice([sub for sub in featureVectors[user].keys() if sub in subToCluster]) 

#     for activityThreshold in activityThresholds:
#         similarUsers = getSimilarUsers(user, sub, 50, activityThreshold)
#         # print activityThreshold, len(similarUsers)
#         total, successes = 0., 0.
#         recommendedSubs = getTopRecs(user, sub, similarUsers, 0.1)

#         for r in recommendedSubs:
#             total += 1
#             if r in featureVectors[user]:
#                 successes += 1
#         if total:       
#             precision[activityThreshold].append(successes * 1.0 / total)

# y = [sum(precision[activityThreshold])/len(precision[activityThreshold]) for activityThreshold in activityThresholds]
# print y

# pyplot.plot(activityThresholds, y)
# pyplot.title('Precision of Recommendations vs. Activity Threshold')
# pyplot.xlabel('Activity threshold for similar users')
# pyplot.ylabel('Precision of recommendations')
# pyplot.show()