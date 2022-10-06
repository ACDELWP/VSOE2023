from pandas import read_csv

data = read_csv('t551_appended.csv')

# remove where t551_TreeStatus is in ['M', 'LF']
data.drop(data.loc[(data.t551_TreeStatus == 'M')].index, inplace=True)
data.drop(data.loc[(data.t551_TreeStatus == 'LF')].index, inplace=True)

# in order to build relative error bars for basal area calculations we need the data.loc[data.Audit == True] entries
# for each of those SamplePointID entries, we'll need to compute total basal area
data_audit = data.loc[data.Audit == True]

# in order to identify the actual dbh entries to be used for basal area calculations we need to drop
# data.loc[data.Audit == True] entries
data.drop(data.loc[data.Audit == True].index, inplace=True)

# now find how many unique years there in data for each SamplePointID in data_audit
# for sp_id in data_audit.SamplePointID.unique():
#    num_years = data.loc[data.SamplePointID == sp_id].year.unique().size
#    if num_years > 1:
#        print(sp_id) # PE2380N2480, PE2768N2588
# there were 2 entries (above) for which multiple year entries are present
# they're revisits from Andrew and should be counted

# now index both dataframes by SamplePointID in order to vectorise the sum calculations
# the relative error bars by bioregion will be fraction of basal area derived from data_audit SamplePointID locations
# relative to the basal area computed from the same SamplePointID locations in data (pi = 3.14)
pi = 3.14
data.set_index([data.SamplePointID.tolist()], inplace=True)
data_audit.set_index([data_audit.SamplePointID.tolist()], inplace=True)
output_file = 'relative_errors_by_bioregion.csv'
header = 'bioregion,error_bar,num_plots,audit_sum,non_audit_sum/n'
with open(output_file, 'w') as w:
    w.writelines(header)

for bioregion in data_audit.BioRegion.unique():
    local_plots = data_audit.loc[data_audit.BioRegion == bioregion].SamplePointID.unique().tolist()
    num_plots = len(local_plots)
    audit_dbh = pi*sum(data_audit.loc[local_plots].t551_DBH)
    data_dbh = pi*sum(data.loc[local_plots].t551_DBH)
    error_bar = abs(audit_dbh - data_dbh)/data_dbh
    output_line = f'{bioregion},{error_bar:.4f},{num_plots},{audit_dbh:.4f},{data_dbh:.4f}\n'
    with open(output_file, 'a') as a:
        a.writelines(output_line)

data.to_csv('t551_for_analysis.csv', index=False)
