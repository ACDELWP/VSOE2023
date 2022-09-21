# F08A: 
Scale and impact of agents and processes affecting forest health and vitality - mortality, dieback, canopy health.

Further details on this work can be accessed in the following JIRA ticket:

https://ffmvic.atlassian.net/browse/MD-256

# Order of operations
## extract_and_append_info_to_t551.py
This procedure extracts the data from the VBMP database, selects the appropriate financial years and 
joins ['Tenure', 'BioRegion'] from the t500 table through the ['SamplePointID'] column in the 
t510 table. This creates the analysis superset from which further cuts will be made. 

## select_analysis_data_subset.py
This procedure introduces further cuts to the analysis superset. It removes ['M', 'LF'] values from t551_TreeStatus 
and most importantly cleans up NaN values in the t551_DBH1/2 columns. This is a crucial step as these 
columns will define the upper and lower bounds of the t551_DBH distribution. In addition, this dataset is the basis 
for the forest health mapping exercise using the kriging method in ArcGIS.

## make_dead_to_total_basal_area_plot.py
This procedure first produces a csv summary of the data that will be plotted.