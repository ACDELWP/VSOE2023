from core import base
from pandas import read_sql

credentials = base.load_user_profile(user='acodoreanu_local', db='vfmp')

engine = base.get_sql_alchemy_engine(host=credentials.server[0],
                                     db=credentials.database[0],
                                     user_name=credentials.username[0],
                                     user_password=credentials.password[0])
connection = engine.connect()

# for more information see MD-256
# tables needed for analysis are 't551_LargeTreeMensuration', '[t500_Location]', [t510_MeasurementEventData]
t500 = read_sql(f"SELECT * FROM [t500_Location]", con=connection)
t551 = read_sql(f"SELECT * FROM [t551_LargeTreeMensuration]", con=connection)
t510 = read_sql(f"SELECT * FROM [t510_MeasurementEventData]", con=connection)

# need to consider measurements between july 1st 2016 and june 30th 2021
# so let's extract the dates from t551_FieldCreatedDate which is of type Timestamp and
# has the following structure: ('2014-04-04 00:00:00')
t551['year'] = t551['t551_FieldCreatedDate'].apply(lambda x: int(str(x).split(' ')[0].split('-')[0]))
t551['month'] = t551['t551_FieldCreatedDate'].apply(lambda x: int(str(x).split(' ')[0].split('-')[1]))
t551['day'] = t551['t551_FieldCreatedDate'].apply(lambda x: int(str(x).split(' ')[0].split('-')[2]))

t551.drop(t551.loc[(t551.year < 2016)].index, inplace=True)
t551.drop(t551.loc[(t551.year == 2016) & (t551.month < 7)].index, inplace=True)
t551.drop(t551.loc[(t551.year == 2021) & (t551.month > 6)].index, inplace=True)

# now, t551 should only have measurements from the respective financial years considered
# next, we need tenure from t500
# in order to connect [t551_MeasurementEventID] with [t500_Tenure]
# I'll need to join [t551_MeasurementEventID] to [t510_SamplePointID] I'll need to go through [t510_MeasurementEventID]
# where t551.t551_MeasurementEventID = t510.t510_MeasurementEventDataID
# could do a join but then I'll need to modify column names. I'll do this the 'slow' way for simplicity and because
# the tables are not that big.

t551['SamplePointID'] = ''
for measurement in t551.t551_MeasurementEventID.unique():
    t551.loc[
        t551.t551_MeasurementEventID == measurement, 'SamplePointID'
    ] = t510.loc[t510.t510_MeasurementEventID == measurement].t510_SamplePointID.unique()[0]

t551['Tenure'] = ''
for samplePoint in t551.SamplePointID.unique():
    t551.loc[
        t551.SamplePointID == samplePoint, 'Tenure'
    ] = t500.loc[t500.t500_SamplePointID == samplePoint].t500_Tenure.unique()[0]

t551['BioRegion'] = ''
for samplePoint in t551.SamplePointID.unique():
    t551.loc[
        t551.SamplePointID == samplePoint, 'BioRegion'
    ] = t500.loc[t500.t500_SamplePointID == samplePoint].t500_IBRA61Bioregion.unique()[0]

t551['VicGridXGIS'] = ''
for samplePoint in t551.SamplePointID.unique():
    t551.loc[
        t551.SamplePointID == samplePoint, 'BioRegion'
    ] = t500.loc[t500.t500_SamplePointID == samplePoint].t500_VicGridXGIS.unique()[0]

t551['VicGridYGIS'] = ''
for samplePoint in t551.SamplePointID.unique():
    t551.loc[
        t551.SamplePointID == samplePoint, 'BioRegion'
    ] = t500.loc[t500.t500_SamplePointID == samplePoint].t500_VicGridYGIS.unique()[0]

t551.to_csv('t551_appended.csv', index=False)
