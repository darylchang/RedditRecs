from collections import defaultdict
from scipy.sparse import csr_matrix
import networkx, pickle

def dot(subA, subB):
	result = 0.
	for user in subA:
		if user in subB:
			result += subA[user] * subB[user]
	return result

def norm(sub):
	return sum([sub[x]**2 for x in sub])**0.5

partition = pickle.load(open('final_partition_subgraphs.pickle'))
featureVectors = defaultdict(dict)
similarityScores = defaultdict(dict)

for line in open('publicvotes-20101018_votes.dump'):
	user, link, sub, vote = line.split()
	if user not in featureVectors[sub]:
		featureVectors[sub][user] = int(vote)
	else:
		featureVectors[sub][user] += int(vote)

for clusterID in range(len(partition)):
	subs = networkx.nodes(partition[clusterID])
	for subA in subs:
		for subB in subs:
			if subA < subB:
				featuresA, featuresB = featureVectors[subA], featureVectors[subB]
				numerator = dot(featuresA, featuresB)
				denominator = norm(featuresA) * norm(featuresB)
				if denominator:
					score = float(numerator) / denominator
				else:
					score = 0.
				print score
				if subA not in similarityScores[clusterID]:
					similarityScores[clusterID][subA] = {subB: score}
				else:
					similarityScores[clusterID][subA][subB] = score

pickle.dump(similarityScores, open('similarity_scores.dump', 'w'))

