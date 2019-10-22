# Author: Aric Hagberg (hagberg@lanl.gov)

#    Copyright (C) 2004-2019 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

import sys

import matplotlib.pyplot as plt
import networkx as nx
import glob
import json

files = glob.glob('./experiments/*.json')

# G = nx.grid_2d_graph(5, 5)  # 5x5 grid


# # print the adjacency list
# for line in nx.generate_adjlist(G):
#     print(line)
# # write edgelist to grid.edgelist



# print(G)


# for i in range(3):
#     G.add_node(i+1)

# G.add_edge(1, 2)

G = nx.DiGraph()

for file in files:
    with open(file, "r") as f:
        experiment = json.load(f)
        G.add_node(experiment["name"])

        for ingredient in experiment["ingredients"]:
            G.add_node(ingredient)
            G.add_edge(experiment["name"], ingredient)


print(experiment)

H = nx.DiGraph(G)


nx.draw(H)
plt.show()
