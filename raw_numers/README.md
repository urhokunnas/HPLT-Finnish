JSON-formatted data where the first word in the filename determines the primary method of classification. 
Eg. tld_output.txt's structure is as follows (abbreviated example):

{"com": "register":{"MT": 1234, "NA-ne": 12355}, "regional_relevance":{"european": 23566, "global": 5678}, 
    "country_relevance": {"finland": 3567, "united_states": 4677}}, "fi": "register: {}, "regional_relevance": {},
      "country_relevance": {}}

register_edu_safety_stats.txt includes data on only content safety and educational value, sorted by register. 
edu_stats.txt and safety_stats.txt include numbers on all other categories.

Values are not sorted in any way. 

Note that a document can have several countries and regions relevant to it, 
so their total value will probably be higher than the total. The total size of the dataset is 51435563 documents. 

The files with noMT in their name exclude documents whose register includes MT (machine translated texts).
The total size of the dataset for those files is 47785741 documents. 
