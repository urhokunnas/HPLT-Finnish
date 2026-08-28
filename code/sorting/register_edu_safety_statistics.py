import json

register_counts = {} 

def n_largest_values(d, N):
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:N]) #d is the dictionary, N is the amount of results 

def give_proportions(dict, total):
    prop_dict = {}
    for key, value in dict.items():
        prop = value / total 
        prop_dict[key] = [value, prop]
    return prop_dict

with open ("C:/Users/shkunn/Downloads/register_edu_safety.txt") as f:
    f = f.read()
    reg_dict = json.loads(f)
    for register, content in reg_dict.items():
        register_counts[register] = {}
        edu = content["educational_value"]
        safety = content["content_safety"]
        total = sum(edu.values())

        edu_highest = n_largest_values(edu, 10)
        safety_highest = n_largest_values(safety, 10)

        edu_prop = give_proportions(edu_highest, total)
        safety_prop = give_proportions(safety_highest, total)
        register_counts[register] = {"total": [total, total / 51435563 ], "educational_value": edu_prop, "content_safety": safety_prop}

register_sorted = dict(sorted(register_counts.items(), key = lambda item: item[1]["total"][0], reverse = True))

with open("C:/Users/shkunn/Documents/results/sorted/register_edu_safety_sorted.txt", "w") as f:
    json.dump(register_sorted, f)

with open("C:/Users/shkunn/Documents/results/sorted/register_edu_safety_sorted.txt") as f:
    file = f.read()
    full = json.loads(file)
    with open("C:/Users/shkunn/Documents/results/top_values/register_edu_safety_stats.txt", "a") as output:
        for key, value in full.items():
            safeties = {k: value["content_safety"][k] for k in list(value["content_safety"])[:5]}
            educations = {k: value["educational_value"][k] for k in list(value["educational_value"])[:5]}

            output.write(f"{key}: Amount of documents: {value["total"]}. \n Top educational values {educations} \n Top safety labels {safeties} \n \n ")

