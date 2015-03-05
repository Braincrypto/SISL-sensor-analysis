from load import *
import matplotlib as mpl
from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt

ed, sd = get_data('0459_2014-10-02')

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

master = None

for ed, sd, name in get_all_data('ids-slide.txt'):
    if master is None:
        master = sd
    else:
        master = pd.concat([master, sd])
    plot_positions(sd, 'imgs/heatmap-position-' + name + '.png')

plot_positions(master, save_filename='imgs/heatmap-position-all.png')
