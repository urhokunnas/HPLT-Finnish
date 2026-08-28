import json
import statistics

tlds = []
country_proportions = {} #countries as keys, lists of proportions in every tld as values 
register_proportions = {}
region_proportions = {}

#EDIT TO BE ABOUT TLD 
standard_devs = {"country": {}, "register": {}, "region": {}}


def give_proportions(dict, total):
    prop_dict = {}
    for key, value in dict.items():
        prop = value / total 
        prop_dict[key] = prop 
    return prop_dict


with open ("C:/Users/shkunn/Downloads/tld_output.txt") as file:
    f = file.read()
    f_json = json.loads(f)
    for tld, content in f_json.items():
        country = content["country_relevance"]
        register = content["register"]
        regions = content["regional_relevance"]
        total = sum(register.values())
        if total < 100: #ignore tlds with less than 100 texts to get more significant results
            continue
        tlds.append({"tld": tld, 
                          "country": give_proportions(country, total), #value: dictionary of key-value pairs: "tld": 0,2 etc.
                          "register": give_proportions(register, total),
                          "region": give_proportions(regions, total) })

for item in tlds:
    for country, value in item["country"].items(): 
        if country in country_proportions.keys():
            country_proportions[country].append(value)
        else:
            country_proportions[country] = [value]
    for register, value in item["register"].items():
        if register in register_proportions.keys():
            register_proportions[register].append(value)
        else:
            register_proportions[register] = [value]
    for region, value in item["region"].items():
        if region in region_proportions.keys():
            region_proportions[region].append(value)
        else:
            region_proportions[region] = [value]

for country, value in country_proportions.items():
    try:
        standard_devs["country"][country] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)} # key: name of country
    except:
        with open ("C:/Users/shkunn/Documents/results/tld_z_score_errors.txt", "a") as f:
            f.write(f"Problem with country {country}\n")
for register, value in register_proportions.items():                                               # value: dictionary of standard deviation and mean of the tld
    try:
        standard_devs["register"][register] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)}
    except:
        with open ("C:/Users/shkunn/Documents/results/tld_z_score_errors.txt", "a") as f:
            f.write(f"Problem with register {register}\n")
for region, value in region_proportions.items():
    try:
        standard_devs["region"][region] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)}
    except:
        with open ("C:/Users/shkunn/Documents/results/tld_z_score_errors.txt", "a") as f:
            f.write(f"Problem with region {region}\n")


country_deviations = []
register_deviations = []
region_deviations = []

for item in tlds: #tlds is a list of dictionaries with nested dictionaries within them
    for country, value in item["country"].items():
        try:
            z_score = (value - standard_devs["country"][country]["mean"] ) / standard_devs["country"][country]["stdev"]
        except:
            continue
        country_deviations.append(
            {"tld": item["tld"],
             "country": country,
             "z-score": z_score,
             "proportion of country in tld": value,
             "mean": standard_devs["country"][country]["mean"],
              "standard deviation": standard_devs["country"][country]["stdev"]  })
    for register, value in item["register"].items():
        try:
            z_score = (value - standard_devs["register"][register]["mean"] ) / standard_devs["register"][register]["stdev"]
        except:
            continue
        register_deviations.append(
            {"tld": item["tld"],
             "register": register,
             "z-score": z_score,
             "proportion of register in tld": value,
             "mean": standard_devs["register"][register]["mean"],
              "standard deviation": standard_devs["register"][register]["stdev"]  })
    for region, value in item["region"].items():
        try:
            z_score = (value - standard_devs["region"][region]["mean"] ) / standard_devs["region"][region]["stdev"]
        except:
            continue
        region_deviations.append(
            {"tld": item["tld"],
             "region": region,
             "z-score": z_score,
             "proportion of region in tld": value,
             "mean": standard_devs["region"][region]["mean"],
              "standard deviation": standard_devs["region"][region]["stdev"]  })

country_deviations.sort(key=lambda x: x["z-score"], reverse=True)
register_deviations.sort(key=lambda x: x["z-score"], reverse=True)
region_deviations.sort(key=lambda x: x["z-score"], reverse=True)


with open ("C:/Users/shkunn/Documents/results/tld_country_z_score.txt", "a") as f:
    f.write("Top 50 tld + country combinations with the largest z-scores:\n")
    for d in country_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/tld_register_z_score.txt", "a") as f:
    f.write("Top 50 tld + register combinations with the largest z-scores:\n")
    for d in register_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/tld_region_z_score.txt", "a") as f:
    f.write("Top 50 tld + region combinations with the largest z-scores:\n")
    for d in region_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

