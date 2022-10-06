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

## create_relative_error_bars_for_basal_area_by_bioregion.py
This procedure introduces further cuts to the analysis superset. It removes ['M', 'LF'] values from t551_TreeStatus 
and drops the Audit == True entries from the analysis file to be used downstream, t551_for_analysis.csv. It also 
computes relative error bars by bioregion. The method for error calculation is further described in code comments.

## make_dead_to_total_basal_area_plot.py
This procedure first produces a csv summary of the data that will be plotted.

## create_samplepointID_CrownDamage_distribution.py
This procedure creates a subset of the t551_appended.csv file created by the *extract_and_append_info_to_t551.py* procedure.

It first extracts the following columns in order to streamline the inputs to the ArcGIS krigging process: 
['SamplePointID', 't551_CreatedByWhom', 'year', 'BioRegion', 'Tenure', 'CrownDamage', 't500_VicGridXGIS', 
't500_VicGridYGIS']. It then computes the average canopy cover for each SamplePointID for each year. If multiple years 
are available, it then only keeps the latest year. At most, there are only 2 years of measurements for a given site.
