from typing import List
import json

from conllup.types import sentenceJson_T
from conllup.conllup import sentenceConllToJson

PATH_FR_CONLLU = "/data/tatoebaAligned/es-fr_small/fr.conllu"
PATH_FR_GMDL = "/data/tatoebaAligned/es-fr_small/fr.gmdl"

with open(PATH_FR_CONLLU, "r") as infile:
    file_text = infile.read()

sentences_conllu = file_text.split("\n\n")

outfile_text = ""
sent_counter = 0
for sentence_conllu in sentences_conllu:
    outfile_text += "t\n"
    
    parsed_sentence = sentenceConllToJson(sentence_conllu)
    vertices = []
    edges = []
    for token in parsed_sentence["treeJson"]["nodesJson"].values():
        upos = token["UPOS"]
        deprel = token["DEPREL"]
        idx = int(token["ID"]) - 1
        head = int(token["HEAD"]) - 1

        vertices.append(f"v {sent_counter}_{idx} {upos}\n")
        if head >= 0:
            edges.append(f"e {sent_counter}_{head} {sent_counter}_{idx} {deprel}\n")
    
    outfile_text += "".join(vertices)
    outfile_text += "".join(edges)

    sent_counter += 1
    if sent_counter == 5:
        break

with open(PATH_FR_GMDL, "w") as outfile:
    outfile.write(outfile_text)