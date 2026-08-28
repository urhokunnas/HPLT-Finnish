import sys
import re
import json
import time

start = time.time()
# The file to be processed
#input_file = sys.argv[1]
input_file = sys.argv[1]
# The file where the TLD distribution is dumped as a JSON object
output_file = sys.argv[2]
time_file = sys.argv[3]
# This regex attempts to match the TLD contained by the URL. Please note that
# the regex is somewhat ad-hoc, so don't rely on it in critical implementations
TLD_regex = re.compile(r'\.([a-zA-Z0-9-]*[a-zA-Z][a-zA-Z0-9-]*)(?:\.(?=[:\/?#]|$)|(?::(?:\d+)?|[\/?#]|$))')
# The TLD distribution is saved here
distr = {}
# Error-raising JSON lines along with their error messages are written here
error_log_file = f"{output_file}.errors"
counter = 0
# This implementation should in principle work with huge files, since Python
# maintains an internal file pointer, and thus the file isn't loaded in memory.
# No chunking or parallelisation is implemented, so expect long runtimes
with open(input_file, 'r', encoding='utf-8')  as file:
    for line in file:
        json_object = json.loads(line)
        counter += 1
        try:
            # Find the TLD in the JSON's URL...
            match = TLD_regex.search(json_object['u']).group(1)
            # find id
            id = json_object['id']
            # ...and the tld and id to the distribution
            distr[id] = match
        except Exception as e:
            # If unable to find tld, mark as no_tld 
            distr[id] = "no_tld"

# Save the distribution to the output file 
    # key-value pairs where the key is the id and the value is the tld 
with open(output_file, 'w') as file:
    json.dump(distr, file)
end = time.time()
print(f'Elapsed: {end - start:.2f} seconds')
print(f"Number of documents processed: {counter}")
