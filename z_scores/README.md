Shows combinations of features that have the largest difference from the mean as measured in standard deviations. 
The first word in the filename shows the sorting category, the second the topic of investigation. For example in
tld_country_z_score.txt, the first line is as follows:

{"tld": "ie", "country": "ireland", "z-score": 14.429720919682968, "proportion of country in tld": 0.34479015918958034, "mean": 0.008200075153729504, "standard deviation": 0.023326167284131092}

The proportion of country in tld shows that 34.4 % of documents with the TLD .ie relate to the country of Ireland. That proportions
is calculated for Ireland in every TLD, and the mean of those is 0.0082. The standard deviation of these means is 0.0233.
The large difference between the mean proportion and proportion in this specific TLD creates a large z-score and indicates this combination is unusual. 

The files starting with noMT exclude documents with MT (machine translated) in the register.
The word _countries_ in the filename indicates that instead of individual countries, statistics are calculated for combinations of countries (as documents can be tagged with multiple countries). 

The 1000 in some filenames involving countries indicates that countries featuring less than 1000 documents were excluded to create more significant results 
(without this filtering the top z-scores tend to involve country tags like the Cook Island, Gibraltar and Isle of Man)
