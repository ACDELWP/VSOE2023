# F08A: 
Scale and impact of agents and processes affecting forest health and vitality - mortality, dieback, canopy health.

Further details on this work can be accessed in the following JIRA ticket:

https://ffmvic.atlassian.net/browse/MD-256

# Order of operations
## extract_and_append_info_to_t551.py
This procedure extracts the data from the VBMP database, selects the appropriate financial years and 
joins ['Tenure', 'BioRegion'] from the t500 table through the ['SamplePointID'] column in the 
t510 table. 

This procedure also introduces the CrownDamage variable which accounts for the 
t551_CrownDefoliated and t551_CrownDiscoloured values. When both columns are defined, then CrownDamage is the sum but when one of the 
columns is undefined, CrownDamage is equal to the defined value. If both columns are undefined then CrownDamage = -99.

This creates the analysis superset from which further cuts will be made. 

## select_analysis_data_subset.py
This procedure introduces further cuts to the analysis superset. It removes ['M', 'LF'] values from t551_TreeStatus 
and most importantly cleans up NaN values in the t551_DBH1/2 columns. This is a crucial step as these 
columns will define the upper and lower bounds of the t551_DBH distribution. 

## make_dead_to_total_basal_area_plot.py
This procedure first produces a csv summary of the data that will be plotted.

## create_samplepointID_CrownDamage_distribution.py
This procedure creates a subset of the t551_appended.csv file created by the *extract_and_append_info_to_t551.py* procedure.

It first extracts the following columns in order to streamline the inputs to the ArcGIS krigging process: 
['SamplePointID', 't551_CreatedByWhom', 'year', 'BioRegion', 'Tenure', 'CrownDamage', 't500_VicGridXGIS', 
't500_VicGridYGIS']. It then computes the average canopy cover for each SamplePointID for each year. If multiple years 
are available, it then only keeps the latest year. At most, there are only 2 years of measurements for a given site.
