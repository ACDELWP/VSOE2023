from pandas import read_csv

data = read_csv('t551_appended.csv')

# extract subset to be used for kriging method
data = data[['SamplePointID', 't551_CreatedByWhom', 'year', 'BioRegion',
             'Tenure', 'CrownDamage', 't500_VicGridXGIS', 't500_VicGridYGIS']]

# drop duplicate entries
data.drop_duplicates(inplace=True)

# drop undefined values
data = data.loc[data.CrownDamage.astype(int) != -99]


# do average by samplepointid, tenure, bioregion, year
for sample_point in data.SamplePointID.unique():
    years = data.loc[data.SamplePointID == sample_point].year.unique().tolist()
    tenures = data.loc[data.SamplePointID == sample_point].Tenure.unique().tolist()
    for year in years:
        for tenure in tenures:
            local_index = data.loc[
                (data.SamplePointID == sample_point) &
                (data.year == year) &
                (data.Tenure == tenure)
            ].index

            local_average = data.loc[local_index].CrownDamage.astype(float).sum()/len(local_index)
            data.loc[local_index, 'CrownDamage'] = local_average


# drop duplicate entries
data.drop_duplicates(inplace=True)

# now just keep the latest year
# do average by SamplePointID, tenure, bioregion, year
for sample_point in data.SamplePointID.unique():
    years = data.loc[data.SamplePointID == sample_point].year.unique().tolist()
    if len(years) > 1:
        # drop the min year entry
        drop_index = data.loc[
            (data.SamplePointID == sample_point) &
            (data.year == min(years))
        ].index

        data.drop(drop_index, inplace=True)

data.sort_values(by=['SamplePointID', 'year'], inplace=True)
data.to_csv('t551_for_kriging_method.csv', index=False)
