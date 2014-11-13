import community
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pickle


# Loading and reading the subgraphs .pickle file
def load_file(filename):
	print 'Loading Final Partition Subgraphs file'
	f = open(filename, 'r')
	subgraphs = pickle.load(f)
	return subgraphs


# Drawing
# Total of 217 separate subgraphs each ranging from 10 to 176 subreddits
def draw_subgraphs(subgraphs):
	count = 0
	num_subgraphs = len(subgraphs)
	for i in range(num_subgraphs):
		figure = plt.figure()
		count += 1.0
		G = subgraphs[i]
		pos = nx.spring_layout(G)

		list_nodes = [nodes for nodes in G.nodes()]
		nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
									node_color = str(count/num_subgraphs))

		nx.draw_networkx_edges(G, pos, alpha=0.5)
		plt.show()
		graph_name = 'graph' + str(count) + '.png'
		figure.savefig(graph_name)


def main():
	subgraphs = load_file('final_partition_subgraphs.pickle')
	draw_subgraphs(subgraphs)


if __name__ == "__main__":
	main()

