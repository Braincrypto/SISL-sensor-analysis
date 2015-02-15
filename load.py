import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

################
# Loading Data #
################

# Defining columns

index_colname = u'time_stamp_ms'
datetime_colname = u'date_time'
session_colname = u'session_id'

meta_colnames = [
    datetime_colname,
    index_colname, 
    session_colname,]

accel_colnames = [ 
    u'accel_x', 
    u'accel_y', 
    u'accel_z',]

touch_finger_colnames = [
    u'touch_finger_id_%d', 
    u'touch_x_%d', 
    u'touch_y_%d', 
    u'touch_phase_%d',]

def get_finger_cols(finger_id):
    return [s % finger_id for s in touch_finger_colnames]

all_touch_finger_colnames = reduce(lambda u, v: u + get_finger_cols(v), range(5), [])
colnames = meta_colnames + accel_colnames + all_touch_finger_colnames

# Reading csv

data = pd.read_csv(
    'data/1.6113_BUTTON_sensor_2014-09-26.csv',
    names=colnames,
    index_col=index_colname,
    skiprows=1,
    sep=',',
)

#############
# Computing #
#############

# Acceleration diff

accel_diff_colnames = [ 
    u'accel_x_diff', 
    u'accel_y_diff', 
    u'accel_z_diff',]

accel_diff_norm_colname = 'accel_diff_norm'
accel_shaking_colname = 'accel_shaking_colname'

def diff_offset(df, cpt_col, res_col, window_size):
    """Computes difference between row i and row i-window_size for all columns in cpt_col.
    Stores result into res_col and return a new dataframe."""
    # We need to drop the index to have a shared int index to compute substraction
    up = df.tail(-window_size).reset_index() 
    down = df.head(-window_size).reset_index()
    # Substract
    up[res_col] = up[cpt_col] - down[cpt_col]
    # Reindex
    up = up.set_index(df.index.name)
    up = up.reindex(df.index)
    return up

# Frequency used to compute the shaking factor
freq = 10

d = diff_offset(data, accel_colnames, accel_diff_colnames, 1)
data[accel_diff_colnames] = d[accel_diff_colnames]

data[accel_diff_norm_colname] = np.square(data[accel_diff_colnames]).sum(axis=1)

cs = data[accel_diff_norm_colname].cumsum()
d = diff_offset(cs, accel_diff_norm_colname, accel_shaking_colname, freq)
data[accel_shaking_colname] = d[accel_shaking_colname]



# freq = 60
# buf = data[accel_colnames].ix[1:freq]
# result = []
# 
# for i in range(freq, len(data)):
#     print("Computing %d" % i)
#     result.append(shaking(buf))
#     buf[freq] = data[accel_colnames].ix[i]
#     buf = buf.ix[1:freq]
# 
# # Select data with touch.
# data_touch = data[data['touch_finger_id_0'].notnull()]
