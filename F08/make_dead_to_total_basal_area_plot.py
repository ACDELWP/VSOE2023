from pandas import read_csv

data = read_csv('t551_for_analysis.csv')
data_error = read_csv('relative_errors_by_bioregion.csv')

# we need breakdowns by bioregion for 'STATE FOREST' and 'PARK/RESERVE'
# save the plot data to csv as well
tenures = ['STATE FOREST', 'PARK/RESERVE']
header = 'tenure,bioregion,' \
         'dead_basal_area,'\
         'dead_basal_area_error,'\
         'total_area,' \
         'total_area_error\n'

with open('basal_area_plot_info.csv', 'w') as w:
    w.writelines(header)

for tenure in tenures:
    for bioregion in data.BioRegion.unique():
        data_subset = data.loc[(data.Tenure == tenure) & (data.BioRegion == bioregion)]
        local_error = data_error.loc[data_error.bioregion == bioregion].error_bar
        print(f'for tenure: {tenure} in BioRegion: {bioregion} we found {data_subset.Tenure.size} records.')
        if data_subset.Tenure.size > 0:
            total_area = data_subset.t551_DBH * data_subset.t551_DBH * 3.14
            total_area = total_area.sum()
            total_area_error = local_error*total_area

            dead_data_subset = data_subset.loc[data_subset.t551_TreeStatus == 'DS']
            dead_basal_area = dead_data_subset.t551_DBH * dead_data_subset.t551_DBH * 3.14
            dead_basal_area = dead_basal_area.sum()
            dead_basal_area_error = dead_basal_area*total_area

            output_line = f'{tenure},{bioregion},' \
                          f'{dead_basal_area},' \
                          f'{dead_basal_area_error}' \
                          f'{total_area,}' \
                          f'{total_area_error}\n'
        else:
            output_line = f'{tenure},{bioregion},0,0,0,0,0,0,0,0\n'

        with open('basal_area_plot_info.csv', 'a') as a:
            a.writelines(output_line)
            print(header.strip('\n'))
            print(output_line)

del data, dead_data_subset, data_subset

plot_data = read_csv('basal_area_plot_info.csv')
plot_data['dead_to_total_ratio'] = plot_data.dead_basal_area / plot_data.total_area
plot_data.loc[plot_data.dead_to_total_ratio.isnull() == True, 'dead_to_total_ratio'] = 0
plot_data['dead_to_total_ratio_m'] = plot_data.dead_basal_area / plot_data.total_area
# now the propagated error for division is:
# error_div = square_root[(error_num/num)^2 + (error_denum/denum)^2]*div_value
# because there is not a uniform +/- error for each point, I'll calculate the
# upper and lower bounds individually.

# upper_bound
plot_data['dead_to_total_ratio_error_p'] = \
    (abs(plot_data.dead_ba_p - plot_data.dead_basal_area) / plot_data.dead_basal_area) ** 2 + \
    (abs(plot_data.total_area_p - plot_data.total_area) / plot_data.total_area) ** 2
plot_data.loc[plot_data.dead_to_total_ratio_error_p.isnull() == True, 'dead_to_total_ratio_error_p'] = 0
plot_data['dead_to_total_ratio_error_p'] = plot_data['dead_to_total_ratio_error_p'] ** 0.5 * plot_data[
    'dead_to_total_ratio']

# lower_bound
plot_data['dead_to_total_ratio_error_m'] = \
    (abs(plot_data.dead_ba_m - plot_data.dead_basal_area) / plot_data.dead_basal_area) ** 2 + \
    (abs(plot_data.total_area_m - plot_data.total_area) / plot_data.total_area) ** 2
plot_data.loc[plot_data.dead_to_total_ratio_error_m.isnull() == True, 'dead_to_total_ratio_error_m'] = 0
plot_data['dead_to_total_ratio_error_m'] = plot_data['dead_to_total_ratio_error_m'] ** 0.5 * plot_data[
    'dead_to_total_ratio']
