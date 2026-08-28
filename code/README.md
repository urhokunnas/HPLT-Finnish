This folder contains code used for processing, filtering, sorting, analysing and visualising HPLT 4.0 Finnish data. All data can be adapted for other language subsets of HPLT 4.0 fairly easily as long as they have similar annotations to the Finnish set. 

`Lumi` is Python files originally run on the Lumi supercomputer. These files were used for processing decompressed HPLT data, which is in .jsonl format. This includes gathering top level domains, adding register labels and so on

`sorting` contains code for pulling the most common categories, eg. the 4 most common TLDs associated with the country of Finland. The outputs are mostly optimised for human readability, not machine readability. 

`differences` has code for calculating z-scores and standard deviations of distributions

`stats` is for getting Chi^2 distances to see which labels affect distributions the most, as well as code for making CSV files, which can be helpful for making charts (can be easily copy-pasted into Excel)
