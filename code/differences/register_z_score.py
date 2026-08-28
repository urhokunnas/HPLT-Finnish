import json
import statistics

registers = []
country_proportions = {} #countries as keys, lists of proportions in every register as values 
tld_proportions = {}
region_proportions = {}

standard_devs = {"country": {}, "tld": {}, "region": {}}


def give_proportions(dict, total):
    prop_dict = {}
    for key, value in dict.items():
        prop = value / total 
        prop_dict[key] = prop 
    return prop_dict


with open ("C:/Users/shkunn/Downloads/register_output_full.txt") as file:
    f = file.read()
    f_json = json.loads(f)
    for register, content in f_json.items():
        country = content["country_relevance"]
        tld = content["tld"]
        regions = content["regional_relevance"]
        total = sum(tld.values())
        if total < 100: #ignore registers with less than 100 texts to get more significant results
            continue
        registers.append({"register": register, 
                          "country": give_proportions(country, total), #value: dictionary of key-value pairs: "tld": 0,2 etc.
                          "tld": give_proportions(tld, total),
                          "region": give_proportions(regions, total) })

for item in registers:
    for country, value in item["country"].items(): 
        if country in country_proportions.keys():
            country_proportions[country].append(value)
        else:
            country_proportions[country] = [value]
    for tld, value in item["tld"].items():
        if tld in tld_proportions.keys():
            tld_proportions[tld].append(value)
        else:
            tld_proportions[tld] = [value]
    for region, value in item["region"].items():
        if region in region_proportions.keys():
            region_proportions[region].append(value)
        else:
            region_proportions[region] = [value]

for country, value in country_proportions.items():
    try:
        standard_devs["country"][country] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)}
    except:
        with open ("C:/Users/shkunn/Documents/results/register_z_score_errors.txt", "a") as f:
            f.write(f"Problem with country {country}\n")
for tld, value in tld_proportions.items():                         
    try:
        standard_devs["tld"][tld] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)}
    except:
        with open ("C:/Users/shkunn/Documents/results/register_z_score_errors.txt", "a") as f:
            f.write(f"Problem with tld {tld}\n")
for region, value in region_proportions.items():
    try:
        standard_devs["region"][region] = {"stdev":statistics.stdev(value), "mean": statistics.mean(value)}
    except:
        with open ("C:/Users/shkunn/Documents/results/register_z_score_errors.txt", "a") as f:
            f.write(f"Problem with region {region}\n")


country_deviations = []
tld_deviations = []
region_deviations = []

for item in registers: #registers is a list of dictionaries with nested dictionaries within them
    for country, value in item["country"].items():
        try:
            z_score = (value - standard_devs["country"][country]["mean"] ) / standard_devs["country"][country]["stdev"]
        except:
            continue
        country_deviations.append(
            {"register": item["register"],
             "country": country,
             "z-score": z_score,
             "proportion of country in register": value,
             "mean": standard_devs["country"][country]["mean"],
              "standard deviation": standard_devs["country"][country]["stdev"]  })
    for tld, value in item["tld"].items():
        try:
            z_score = (value - standard_devs["tld"][tld]["mean"] ) / standard_devs["tld"][tld]["stdev"]
        except:
            continue
        tld_deviations.append(
            {"register": item["register"],
             "tld": tld,
             "z-score": z_score,
             "proportion of tld in register": value,
             "mean": standard_devs["tld"][tld]["mean"],
              "standard deviation": standard_devs["tld"][tld]["stdev"]  })
    for region, value in item["region"].items():
        try:
            z_score = (value - standard_devs["region"][region]["mean"] ) / standard_devs["region"][region]["stdev"]
        except:
            continue
        region_deviations.append(
            {"register": item["register"],
             "region": region,
             "z-score": z_score,
             "proportion of region in tld": value,
             "mean": standard_devs["region"][region]["mean"],
              "standard deviation": standard_devs["region"][region]["stdev"]  })

country_deviations.sort(key=lambda x: x["z-score"], reverse=True)
tld_deviations.sort(key=lambda x: x["z-score"], reverse=True)
region_deviations.sort(key=lambda x: x["z-score"], reverse=True)


with open ("C:/Users/shkunn/Documents/results/register_country_z_score.txt", "a") as f:
    f.write("Top 50 register + country combinations with the largest z-scores:\n")
    for d in country_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/register_tld_z_score.txt", "a") as f:
    f.write("Top 50 register + tld combinations with the largest z-scores:\n")
    for d in tld_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/register_region_z_score.txt", "a") as f:
    f.write("Top 50 register + region combinations with the largest z-scores:\n")
    for d in region_deviations[:50]:
       json.dump(d,f)
       f.write("\n\n")

