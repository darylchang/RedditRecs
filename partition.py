import community
import networkx as nx
import matplotlib.pyplot as plt
import pickle

print 'Reading edge list'
G = nx.read_adjlist('edge_list_smaller.txt')
# G = nx.erdos_renyi_graph(2000, 0.02)

# First compute the best partition
print 'Partitioning'

final = []
todo = [G]
deleted = 0

while todo:
	currentSubgraph = todo.pop(0)
	partition = community.best_partition(currentSubgraph)
	clusters = {}
	for subreddit in partition.keys():
		clusterID = partition[subreddit]
		if clusterID not in clusters:
			clusters[clusterID] = [subreddit]
		else:
			clusters[clusterID].append(subreddit)
	if len(clusters.items()) == 1:
		final.append(currentSubgraph)
		continue

	for clusterID, nodes in clusters.items():
		subgraph = currentSubgraph.subgraph(nodes)
		if len(subgraph.nodes()) < 10:
			print "discarding sub with l=", len(subgraph.nodes())
			deleted += len(subgraph.nodes())
			continue
		elif len(subgraph.nodes()) < 100:
			print "adding sub with l=", len(subgraph.nodes())
			final.append(subgraph)
		else:
			print "expanding sub with l=", len(subgraph.nodes())
			todo.append(subgraph)

pickle.dump(final, open('final_partition_subgraphs.pickle', 'w'))

print [len(graph.nodes()) for graph in final]
print deleted
