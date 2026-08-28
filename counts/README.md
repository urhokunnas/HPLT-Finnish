The folder counts contains files with dictionaries. The name of each file ending in `_output.txt` shows the main-level keys of the dictionary, and the values are dictionaries showing how many documents are present with each combination of labels. Everything except TLDs, crawls and FinePDFs values are from Propella annotations. 
The following is a simplified example from tld_output.txt. Note that the results are not sorted in any way. As each document can have multiple country_relevance or regional_relevance labels the total of those categories does not reflect the total amount of documents. Instead, top level domain and register can be used to count the total amount of documents in a category, as each document has exactly one of both. 

`{"com": {"register": {"MT": 1575693, "no-label": 109893, "ID": 300597, "IN": 230399, "IP-ds": 2767045, "IN-MT": 82207}, "regional_relevance": {"european": 11000041, "culturally_neutral": 822047, "russian_sphere": 249842},"country_relevance": {"finland": 10137550, "estonia": 112088, "none": 1412045, "germany": 371129}, "fi": {"register":{}, "regional_relevance":{}, "country_relevance":{}}}`

The files with noMT in the name exclude any files with the MT register (using probability of 0.4 as a limit), including hybrids.  

Note that results are not ordered in any way. 

List and overview of dictionary structure for each file:

- `business_sector.txt`: Business sectors as main keys, values are dictionaries "tld", "register", "country_relevance", "regional_relevance" "content_safety", and "educational_value". Inside these dictionaries the keys are strings like "com" or "argentina" and values integers.
- `country_output.txt` Countries as main keys, values dictionaries "register", "tld", "regional_relevance". 
- `country_output_noMT.txt`, is the same except documents with MT in their register (hybrid or not) are excluded
- `countries_together_output.txt` and `countries_together_noMT.txt` follow the same formula as the two above, except rather than counting just how many times each country is present in document metadata they also contain combinations of countries in the keys, such that if a document's metadata has country_relevance as ["finland", "sweden"], the document will be included under the key "finland-sweden"
- `crawl_output.txt`: main keys names of crawls ("archivebot","CC-MAIN-2021-31" etc. ), below that a layer of Propella educational_value scores and within each the following keys: "register", "tld", "safety", "country" and "region"
- `edu_output.txt`: main keys Propella educational_value labels, values dictionaries "register", "tld", "regional_relevance", "country_relevance" and "content_safety"
- `finepdfs_edu_output.txt`: the numbers -0 to 5 as keys, matching the value given to the texts by the FinePDFs-Edu filter, where -0 is -1 to 0, 0 is 0-1, 1 is 1-2 etc. This is sort of an arbitrary grouping, as FinePDFs instructions recommend using the top 10% of documents as sorted by value, but can be used for a simplified overview. Values are the following dictionaries: "prop_edu" (Propella educational_value), "register", "business" (Propella business_sector), "quality" (Propella content_quality)
- `MT_probability.txt` has a key-value pair for every document with MT in the register. The key is the year (based on CC crawl) and the value is a list [register, MT probability]
- `quality_output.txt`: keys are Propella content_quality labels, values dictionaries "edu" (Propella educational_value), "type" (Propella content_type), "register"
- `region_output.txt`: main keys regions, values dictionaries "register", "tld", "country_relevance"
- `region_output_noMT.txt` is the same without MT texts
- `register_edu_safety.txt`: main keys are registers, values dictionaries "educational_value" and "content_safety" 
- `register_output.txt`: main keys are registers, values dictionaries "tld", "regional_relevance" and "country_relevance". `register_output_noMT.txt` is the same without MT registers
- `safety_output.txt` has Propella content_safety labels as main keys, with dictionaries "register", "tld", "regional_relevance", "country_relevance" and "educational_value"
- `tld_output.txt` has top level domains as keys, with dictionaries "register", "regional_relevance" and "country_relevance". `tld_output_noMT.txt` is the same but without documents with MT or MT hybrids as the register. 