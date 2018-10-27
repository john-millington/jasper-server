#!/usr/bin/env python
# encoding: utf-8

import pytextrank
import sys
import os

## Stage 1:
##  * perform statistical parsing/tagging on a document in JSON format
##
## INPUTS: <stage0>
## OUTPUT: JSON format `ParsedGraf(id, sha1, graf)`

if __name__ == "__main__":
    path_stage0 = sys.argv[1]
    path_stage1 = 'temp.json'

    with open(path_stage1, 'w') as f:
        for graf in pytextrank.parse_doc(pytextrank.json_iter(path_stage0)):
            f.write("%s\n" % pytextrank.pretty_print(graf._asdict()))
    
    graph, ranks = pytextrank.text_rank(path_stage1)
    pytextrank.render_ranks(graph, ranks)

    for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
        # to view output in this notebook
        print(pytextrank.pretty_print(rl))

    # os.remove(path_stage1)