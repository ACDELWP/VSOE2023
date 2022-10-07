import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pandas import read_csv
from os.path import isfile

def make_plot(local_subplot, local_plot_id, bioregion, colours, frag_categories, y_tick_locations, y_ticks, logfile):

    local_plot = local_subplot[local_plot_id[0], local_plot_id[1]]
    y_offset = np.zeros(4)
    sub_plot_data = data.loc[data.bioregion == bioregion]
    for frag_cat in frag_categories:
        plot_subset = sub_plot_data.loc[sub_plot_data.frag_category == frag_cat]

        for local_label in plot_subset.label.unique().tolist():
            plot_subset.loc[
                plot_subset.label == local_label, 'local_area_pct'
            ] = plot_subset.loc[plot_subset.label == local_label].local_area_pct.sum()

        plot_subset.drop_duplicates(subset=['label'], inplace=True)
        x_data = list(plot_subset.label)
        plot_data = list(plot_subset.local_area_pct)
        local_plot.set_title(bioregion)
        local_plot.grid(axis='y', linestyle='--', color='black')
        local_plot.set_yticks(y_tick_locations)
        local_plot.set_yticklabels(y_ticks)
        local_plot.set_ylim([0, 1.1])
        local_plot.bar(x_data, plot_data, bottom=y_offset, color=colours[frag_cat])
        y_offset = y_offset + plot_data

        if not isfile(logfile):
            logfile_header = 'bioregion,frag_category,'
            logfile_header = logfile_header + ','.join(str(x_data_item) for x_data_item in list(x_data)) + '\n'
            print(logfile_header)
            with open(logfile, 'w') as w:
                w.writelines(logfile_header)

        with open(logfile, 'a') as a:
            local_log_line = f'{bioregion},{frag_cat},'
            local_log_line = local_log_line + ','.join(str(x_data_item) for x_data_item in list(plot_data)) + '\n'
            print(local_log_line)
            a.writelines(local_log_line)

        if local_plot_id[0] == 3:
            if local_plot_id[1] == 0:
                local_subplot[3, 0].set_xticklabels(x_data, rotation=45)
            if local_plot_id[1] == 1:
                local_subplot[3, 1].set_xticklabels(x_data, rotation=45)
            if local_plot_id[1] == 2:
                local_subplot[3, 2].set_xticklabels(x_data, rotation=45)


data = read_csv('table_plot_data.csv')
output_log_file = 'f04_fragmentation_by_bioregion_2022.csv'
output_image_name = 'f04_fragmentation_by_bioregion_2022.jpg'

# add gridcode labels
# Grid code 1 - Patch | 2 - Transitional | 3 - Perforated | 4 - Edge | 5 - Interior | 0=nonforest
data['frag_category'] = ''
data.loc[data.gridcode == 1, 'frag_category'] = 'Patch'
data.loc[data.gridcode == 2, 'frag_category'] = 'Transitional'
data.loc[data.gridcode == 3, 'frag_category'] = 'Perforated'
data.loc[data.gridcode == 4, 'frag_category'] = 'Edge'
data.loc[data.gridcode == 5, 'frag_category'] = 'Interior'
data.loc[data.gridcode == 0, 'frag_category'] = 'Non Forest'

fragmentation_categories = data.frag_category.unique().tolist()

# setup color codes to be used in plots
color_codes = {
    'Patch': 'darkkhaki',
    'Transitional': 'aquamarine',
    'Edge': 'slategray',
    'Perforated': 'lightcoral',
    'Interior': 'forestgreen',
    'Non Forest': 'navy'
}

bioregions = data.bioregion.unique()
x_tick_location = [1, 2, 3, 4]
blank_x_ticks = ['', '', '', '']
ytick_locations = [0.2, 0.4, 0.6, 0.8, 1.0]
y_tick_marks = ['20%', '40%', '60%', '80%', '100%']
plot_locations = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2], [3, 0], [3, 1], [3, 2]]

matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
fig, axs = plt.subplots(4, 3, figsize=(20, 15))
for index, local_bioregion in enumerate(bioregions):
    print(index, plot_locations[index], local_bioregion)
    make_plot(
        axs, plot_locations[index], local_bioregion, color_codes,
        fragmentation_categories, ytick_locations, y_tick_marks, output_log_file
    )

for ax in fig.get_axes():
    ax.label_outer()

# ok, now set up the legend in axs[0, 2]
axs[0, 2].axis('off')
for index, frag_category in enumerate(fragmentation_categories):
    local_color = color_codes[frag_category]
    # now plot a thick line from 1 to 2 at 0.3 + index/10
    axs[0, 2].plot([1, 1.2], [0.3 + index / 10, 0.3 + index / 10], linewidth=15, color=local_color)
    axs[0, 2].text(1.4, 0.3 + index / 10 - 0.03, frag_category, fontsize=14)
    axs[0, 2].set_ylim([0, 1.1])
    axs[0, 2].set_xlim([0, 3])

    axs[0, 2].text(0.9, 0.8, 'Fragmentation Category', fontsize=14)

fig.savefig(output_image_name)
