import json
import sys

num = 0
ids = ["d4e4879b58f17a1dfa3d20c546934ac9", "34a5c749acfe08c9927eac10a285d431"]
output = []
with open (sys.argv[1], "r") as f:
    for line in f: 
        if num == 2:
            break
        doc = json.loads(line)
        if doc["id"] in ids:
            output.append(doc)
            num += 1 


with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/example_metadata.txt", "a") as f:
    json.dump(output, f)

