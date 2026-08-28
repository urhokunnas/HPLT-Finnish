These files use Plotly and Pandas to visualise data about HPLT4.0 Finnish in various ways. 

The folder `plotly_examples` contains basic examples for creating various types of plots, with a lot of comments as explanation. 

The others have fairly self-explanatory names showing which aspects they plot against each other. Most of the results are simple bar charts, but the following scripts produce something different:
- `yearly_register_edu_facets.py` creates a faceted bar chart with several rows
- `MT_probability.py` creates a boxplot and a faceted histogram showing how the strength of machine translation predictions changes by year
- `MT_hybrids_fp.py` creates a faceted bar plot separating educational scores from Propella and FinePDFs
- `edu_bar_pie.py` creates both a bar chart and a pie chart in the same view
