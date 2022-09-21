#Fo:04
Fragmentation of native forest cover.

Further details on this work can be accessed in the following JIRA ticket:

https://ffmvic.atlassian.net/browse/MD-252

#Order of operations

##create_plot_data_table.py
This procedure reads the initial data source and combines the MMTGEN variables into the reporting subset. It then groups 
area by bioregion, MMTGEN derived label and gridcode. Finally, it computes relative fraction at
(bioregion) & (MMTGEN derived label) level and saves it to a csv file.

##plot_data.py
This procedure reads in the above csv file and creates a 3x4 panel plot. It also logs the exact numerical values used 
in the plot itself.