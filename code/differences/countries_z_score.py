import json
import statistics

countries = []
tld_proportions = {} #tlds as keys, lists of proportions in every country as values 
register_proportions = {}
region_proportions = {}


standard_devs = {"tld": {}, "register": {}, "region": {}}


def give_proportions(dict, total):
    prop_dict = {}
    for key, value in dict.items():
        prop = value / total 
        prop_dict[key] = prop 
    return prop_dict


with open ("C:/Users/shkunn/Downloads/countries_together_output.txt") as file:
    f = file.read()
    f_json = json.loads(f)
    for country, content in f_json.items():
        tld = content["tld"]
        register = content["register"]
        regions = content["regional_relevance"]
        total = sum(tld.values())
        if total < 100: #ignore countries with less than 100 texts to get more significant results
            continue
        countries.append({"country": country, 
                          "tld": give_proportions(tld, total), #value: dictionary of key-value pairs: "tld": 0,2 etc.
                          "register": give_proportions(register, total),
                          "region": give_proportions(regions, total) })

for item in countries:
    for tld, value in item["tld"].items(): 
        if tld in tld_proportions.keys():
            tld_proportions[tld].append(value)
        else:
            tld_proportions[tld] = [value]
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

for tld, value in tld_proportions.items():
    try:
        standard_devs["tld"][tld] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)} # key: name of tld
    except:
        with open ("C:/Users/shkunn/Documents/results/z_score_errors.txt", "a") as f:
            f.write(f"Problem with tld {tld}\n")
for register, value in register_proportions.items():                                               # value: dictionary of standard deviation and mean of the tld
    try:
        standard_devs["register"][register] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)}
    except:
        with open ("C:/Users/shkunn/Documents/results/z_score_errors.txt", "a") as f:
            f.write(f"Problem with register {register}\n")
for region, value in region_proportions.items():
    try:
        standard_devs["region"][region] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)}
    except:
        with open ("C:/Users/shkunn/Documents/results/z_score_errors.txt", "a") as f:
            f.write(f"Problem with region {region}\n")


tld_deviations = []
register_deviations = []
region_deviations = []

for item in countries: #countries is a list of dictionaries with nested dictionaries within them
    for tld, value in item["tld"].items():
        try:
            z_score = (value - standard_devs["tld"][tld]["mean"] ) / standard_devs["tld"][tld]["stdev"]
        except:
            continue
        tld_deviations.append(
            {"country": item["country"],
             "tld": tld,
             "z-score": z_score,
             "proportion of tld in country": value,
             "mean": standard_devs["tld"][tld]["mean"],
              "standard deviation": standard_devs["tld"][tld]["stdev"]  })
    for register, value in item["register"].items():
        try:
            z_score = (value - standard_devs["register"][register]["mean"] ) / standard_devs["register"][register]["stdev"]
        except:
            continue
        register_deviations.append(
            {"country": item["country"],
             "register": register,
             "z-score": z_score,
             "proportion of register in country": value,
             "mean": standard_devs["register"][register]["mean"],
              "standard deviation": standard_devs["register"][register]["stdev"]  })
    for region, value in item["region"].items():
        try:
            z_score = (value - standard_devs["region"][region]["mean"] ) / standard_devs["region"][region]["stdev"]
        except:
            continue
        region_deviations.append(
            {"country": item["country"],
             "region": region,
             "z-score": z_score,
             "proportion of region in country": value,
             "mean": standard_devs["region"][region]["mean"],
              "standard deviation": standard_devs["region"][region]["stdev"]  })

tld_deviations.sort(key=lambda x: x["z-score"], reverse=True)
register_deviations.sort(key=lambda x: x["z-score"], reverse=True)
region_deviations.sort(key=lambda x: x["z-score"], reverse=True)


with open ("C:/Users/shkunn/Documents/results/countries_tld_z_score.txt", "a") as f:
    f.write("Top 50 country + tld combinations with the largest z-scores:\n")
    for d in tld_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/countries_register_z_score.txt", "a") as f:
    f.write("Top 50 country + register combinations with the largest z-scores:\n")
    for d in register_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/countries_region_z_score.txt", "a") as f:
    f.write("Top 50 country + region combinations with the largest z-scores:\n")
    for d in region_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

