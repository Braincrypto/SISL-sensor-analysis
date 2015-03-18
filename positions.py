from load import *
import matplotlib as mpl
from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt

def get_positions(data):
    if 'touch_x_0' in data.columns:
        filtered_data = data[['touch_x_0','touch_y_0']].dropna()
        return filtered_data['touch_x_0'], filtered_data['touch_y_0']    

    else:
        position_data = data[data['sensor_type'] == 'MOUSE']
        filtered_data = position_data[['v1','v2']].dropna().drop_duplicates()
        return filtered_data['v1'], filtered_data['v2']    


def plot_positions(x, y, save_filename=None):
    fig = plt.figure()
    plt.hist2d(x, y, bins=100, cmap=mpl.cm.rainbow)
    plt.colorbar()
    if save_filename is None:
        plt.show()
    else:
        print('Saving file [%s]' % (save_filename,))
        plt.savefig(save_filename)
        plt.close(fig)

exp_types = [
    'button', 
    'slide',
]


for exp_type in exp_types:
    print('Loading experiment [%s]' % exp_type)

    master = None
    for event_data, sensor_data, file_name in get_all_data('ids-%s-selected.txt' % exp_type):
        x, y = get_positions(sensor_data)
        positions = pd.concat([x, y], axis=1)
        positions.columns = ['x', 'y']

        if master is None:
            master = positions
        else:
            master = pd.concat([master, positions])

        plot_positions(x, y, 'imgs/heatmap-position-' + file_name + '.png')

    plot_positions(master.x, master.y, save_filename='imgs/heatmap-position-%s-all.png' % exp_type)
