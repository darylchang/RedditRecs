import community
import networkx as nx
import matplotlib.pyplot as plt

print 'Reading edge list'
G = nx.read_adjlist('edge_list.txt.gz')

#first compute the best partition
print 'Partitioning'
partition = community.best_partition(G)
nx.write_adjlist(partition, 'partition_edge_list.txt.gz')

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))

nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()