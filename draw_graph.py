import community
import networkx as nx
import matplotlib.pyplot as plt
import pickle


# Loading and reading the subgraphs .pickle file
def load_file(filename):
	print 'Loading Final Partition Subgraphs file'
	f = open(filename, 'r')
	subgraphs = pickle.load(f)
	return subgraphs


# Drawing subgraphs
# Total of 217 separate subgraphs each ranging from 10 to 176 subreddits
def draw_subgraphs(subgraphs):
	count = 0
	num_subgraphs = len(subgraphs)
	for i in range(num_subgraphs):
		count += 1.0
		G = subgraphs[i]
		pos = nx.spring_layout(G)

		list_nodes = [nodes for nodes in G.nodes()]
		num_nodes = len(list_nodes)
		num_edges = G.number_of_edges()

		plt.figure()

		nx.draw(G,pos,node_color=range(num_nodes),node_size=100, cmap=plt.cm.Blues,
			edge_color=range(num_edges), edge_cmap=plt.cm.Blues)

		graph_name = 'graph' + str(count) + '.png'
		
		plt.savefig(graph_name)
		plt.show()


def main():
	subgraphs = load_file('final_partition_subgraphs.pickle')
	draw_subgraphs(subgraphs)


if __name__ == "__main__":
	main()

