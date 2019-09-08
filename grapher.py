import os
import json

import networkx as nx

with open("sponsors.json") as f:
    sponsors = json.load(f)

sponsor_pairs = [(key, value) for key in sponsors.keys() for value in sponsors[key]]

graph = nx.Graph()

for pair in sponsor_pairs:
    graph.add_node(pair[0], color="#BA68C8")
    graph.add_node(pair[1], color="#FFD54F")
    graph.add_edge(*pair)

agraph = nx.nx_agraph.to_agraph(graph)
agraph.layout("neato", args="-Goverlap=scalexy -Gsplines=true")
agraph.draw("sponsors.png")
