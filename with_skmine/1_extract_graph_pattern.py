from typing import List
import json

from conllup.types import sentenceJson_T
import networkx as nx
from skmine.graph.graphmdl.graph_mdl import GraphMDL
from skmine.graph.graphmdl import utils


PATH_FR_PARSING = "/data/tatoebaAligned/es-fr_small/fr.parsing"


parsed_sentences: List[sentenceJson_T] = []
data_graph = nx.DiGraph() # Create new directed graph
data_graph.add_node("-1")
data_graph.nodes["-1"]["label"] = "ANCHOR"
with open(PATH_FR_PARSING, "r") as infile:
    sent_counter = 0
    for line in infile:
        
        if sent_counter == 50:
            break

        parsed_sentence: sentenceJson_T = json.loads(line)["parsingJson"]
        parsed_sentences.append(parsed_sentence)
        for token in parsed_sentence["treeJson"]["nodesJson"].values():
            unique_name = f"{sent_counter}_{token['ID']}"
            unique_name_head = f"{sent_counter}_{token['HEAD']}"
            data_graph.add_node(unique_name)
            if token["HEAD"] == 0:
                data_graph.add_edge("-1", unique_name, label=f"anchor_{sent_counter}")
            else:
                data_graph.add_edge(unique_name_head, unique_name, label=token["DEPREL"])
            data_graph.nodes[unique_name]['label'] = token["UPOS"]

        
        sent_counter += 1


graphmdl = GraphMDL() # Initialize the approach
graphmdl.fit(data_graph, timeout=250) # Run the approach on the data graph. Timeout is optional and in seconds.

patterns: List[nx.DiGraph] = list(graphmdl.patterns())

def get_label(obj):
    obj.get('label', 'ANY')


for pattern in patterns:
    print(pattern.nodes(data=True))
    nodes_labels = pattern.nodes.data()
    for (u, v, label) in pattern.edges.data('label'):
        u_upos = pattern.nodes[u].get("label", "ANY")
        v_upos = pattern.nodes[v].get("label", "ANY")
        print(f"({u_upos}, {v_upos}, {label})")
    print()

print("Number of selected patterns",len(patterns))


print(f"initial description length = {graphmdl.initial_description_length()}")
print(f"Final description length = {graphmdl.description_length()}")
print(f"Compression ratio = {round((graphmdl.description_length()/ graphmdl.initial_description_length())*100, 2)} %")