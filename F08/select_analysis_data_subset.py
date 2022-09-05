from pandas import read_csv

data = read_csv('t551_appended.csv')

# remove where t551_TreeStatus is in ['M', 'LF']
data.drop(data.loc[(data.t551_TreeStatus == 'M')].index, inplace=True)
data.drop(data.loc[(data.t551_TreeStatus == 'LF')].index, inplace=True)

# replace Nan values in t551_DBH1 or t551_DBH2 with t551_DBH in order to build some error bounds
# DBH1 = DBH - (DBH2 - DBH)
dbh1_nulls = data.loc[data.t551_DBH1.isnull() == True].index
dbh2_nulls = data.loc[data.t551_DBH2.isnull() == True].index
print(f'DBH1 is null in {dbh1_nulls.size} locations \n'
      f'DBH2 is null in {dbh2_nulls.size} locations')

data.loc[dbh1_nulls, 't551_DBH1'] = \
       data.loc[dbh1_nulls, 't551_DBH'] - \
       (abs(data.loc[dbh1_nulls, 't551_DBH2'] - data.loc[dbh1_nulls, 't551_DBH']))

data.loc[dbh2_nulls, 't551_DBH2'] = \
      data.loc[dbh2_nulls, 't551_DBH'] - \
      (abs(data.loc[dbh2_nulls, 't551_DBH1'] - data.loc[dbh2_nulls, 't551_DBH']))

print('Basal are sums:')
print(data.t551_DBH2.sum(), data.t551_DBH.sum(), data.t551_DBH1.sum())



