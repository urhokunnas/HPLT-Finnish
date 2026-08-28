import json
import sys
import os

propella_dir = sys.argv[1]

propella_filenames = os.listdir(propella_dir)
propella_list = []
for item in propella_filenames:
    name = propella_dir + "/" + item
    propella_list.append(name)

counter = 0

#with open ("/scratch/project_462001491/urho/hplt_4.0/metadata/hplt_finnish.txt", "a") as output:

for f in propella_list:
    file = open(f)
    filename = "/scratch/project_462001491/urho/hplt_4.0/metadata/hplt_finnish" + str(counter) + ".txt"
    with open (filename,"a") as output:
        for line in file:
            j = json.loads(line)
            j.pop("text")
            j.pop("xml")
            j.pop("md")
            json.dump(j, output)
    counter += 1
