from pandas import read_csv


data = read_csv('FF_20220829_1700.csv')

# assign 'PRIVATE' labels
data.loc[data.loc[data.MMTGEN.isnull() == True].index.tolist(), 'MMTGEN'] = 'PRIVATE'

# remove rows that will not be used in the analysis
data.drop(
    index=data.loc[data.GENER_DESC == 'MARINE'].index.tolist(),
    inplace=True
)
data.drop(
    index=data.loc[data.GENER_DESC.isnull() == True].index.tolist(),
    inplace=True
)
data.drop(
    index=data.loc[data.gridcode == 0].index.tolist(),
    inplace=True
)
data.drop(
    index=data.loc[data.bioregion.isnull() == True].index.tolist(),
    inplace=True
)

# harmonise MMTGEN field to reflect the 4 reporting categories
data['label'] = ''
data.loc[data.MMTGEN == 'NATIONAL PARKS ACT AND NATURE CONSERVATION RESERVES', 'label'] = 'Parks & Reserves'
data.loc[data.MMTGEN == 'OTHER CONSERVATION RESERVES', 'label'] = 'Parks & Reserves'
data.loc[data.MMTGEN == 'STATE FOREST', 'label'] = 'State Forest'
data.loc[data.MMTGEN == 'PLANTATION', 'label'] = 'State Forest'
data.loc[data.MMTGEN == 'PRIVATE', 'label'] = 'Private'
data.loc[data.MMTGEN == 'COMMONWEALTH LAND', 'label'] = 'Other Crown Land'
data.loc[data.MMTGEN == 'OTHER PUBLIC LAND', 'label'] = 'Other Crown Land'

# select column subset for analysis
table_data = data[['bioregion', 'gridcode', 'label', 'AREA_HA']]
del data


table_plot_data_name = 'f04_plot_data.csv'
with open(table_plot_data_name, 'w') as w:
    header = 'bioregion,gridcode,label,local_area,local_area_pct,sum_area\n'
    w.writelines(header)

# summarise the area for each bioregion and then get fraction of each gridcode for each label
for bioregion in table_data.bioregion.unique():
    subset = table_data.loc[table_data.bioregion == bioregion]
    for label in table_data.label.unique():
        sum_area = subset.loc[subset.label == label].AREA_HA.sum()
        for gridcode in table_data.gridcode.unique():
            local_area = subset.loc[(subset.gridcode == gridcode) &
                                    (subset.label == label)
                                    ].AREA_HA.sum()
            # 'bioregion,gridcode,gridcode_name,MMGTGEN,local_area,local_area_pct,sum_area\n'
            output_line = f'{bioregion},{gridcode},{label},{local_area},{local_area / sum_area},{sum_area}\n'
            with open(table_plot_data_name, 'a') as a:
                a.writelines(output_line)
                print(output_line)

print(f'finished writing plot data to: {table_plot_data_name}')