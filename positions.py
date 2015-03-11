from load import *
import matplotlib as mpl
from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt


def plot_positions(sensor_data, save_filename=None):
    filtered_data = sensor_data[['touch_x_0','touch_y_0']].dropna()
    x, y = filtered_data['touch_x_0'], filtered_data['touch_y_0']
    fig = plt.figure()
    plt.hist2d(x, y, bins=100, cmap=mpl.cm.rainbow)
    plt.colorbar()
    if save_filename is None:
        plt.show()
    else:
        print('Saving file [%s]' % (save_filename,))
        fig.savefig(save_filename)
        plt.close(fig)

exp_types = ['button', 'slide']


for exp_type in exp_types:
    print('Loading experiment [%s]' % exp_type)

    master = None
    for event_data, sensor_data, file_name in get_all_data('ids-%s.txt' % exp_type):
        if master is None:
            master = sensor_data
        else:
            master = pd.concat([master, sensor_data])
        plot_positions(sensor_data, 'imgs/heatmap-position-' + file_name + '.png')

    plot_positions(master, save_filename='imgs/heatmap-position-%s-all.png' % exp_type)
