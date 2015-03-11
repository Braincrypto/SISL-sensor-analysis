import pandas as pd

################
# Loading Data #
################

# Defining columns

index_colname = u'time_stamp_ms'
datetime_colname = u'date_time'
session_colname = u'session_id'

meta_colnames = [
    datetime_colname,
    index_colname,]

accel_colnames = [ 
    u'accel_x', 
    u'accel_y', 
    u'accel_z',]

touch_finger_colnames = [
    u'touch_finger_id_%d', 
    u'touch_x_%d', 
    u'touch_y_%d', 
    u'touch_phase_%d',]

trial_row_id_colname = u'trial_row_id'
trial_value_colname = u'trial_value'

trial_colnames = [
    trial_row_id_colname,
    trial_value_colname,
]

event_type_colname = u'event_type'
event_value_colname = u'event_value'

event_colnames = [
    event_type_colname,
    event_value_colname,
]

key_correct_colname = "key_correct"
key_incorrect_colname = "key_incorrect"
miss_colname = "miss"
success_colname = "success"
success_aggregate_colname = "success_aggregate"

cue_pos_px_colnames = [
    u'cue_pos_x_pixels',
    u'cue_pos_y_pixels',
]

cue_pos_norm_colnames = [
    u'cue_pos_x_norm',
    u'cue_pos_y_norm',
]

cue_vy_norm_colname = u'cue_vy_norm'

cue_colnames = cue_pos_px_colnames + cue_pos_norm_colnames + [cue_vy_norm_colname]

cursor_pos_x_px = u'cursor_pos_x_pixels'
cursor_vx_colname = u'cursor_vx'

cursor_colnames = [cursor_pos_x_px, cursor_vx_colname]

def get_finger_cols(finger_id):
    return [s % finger_id for s in touch_finger_colnames]

all_touch_finger_colnames = reduce(lambda u, v: u + get_finger_cols(v), range(5), [])
sensor_colnames = meta_colnames + [session_colname] + accel_colnames + all_touch_finger_colnames
event_colnames = meta_colnames + trial_colnames + event_colnames + cue_colnames + cursor_colnames + [session_colname]

# Reading csv

def get_data(name):
    sensor_data = pd.read_csv(
        u'data/sensor.%s' % name,
        names=sensor_colnames,
        index_col=index_colname,
        skiprows=1,
        sep=',',
        low_memory=False,
    )

    event_data = pd.read_csv(
        u'data/event.%s' % name,
        #names=event_colnames,
        index_col=index_colname,
        #skiprows=1,
        sep=",",
        low_memory=False,
    )

    return event_data, sensor_data

def get_all_data(list_file):
    with open(list_file) as f:
        for line in f.readlines():
            name = line.strip()
            if name[0] == '#':
                continue

            ed, sd = get_data(name)
            yield ed, sd, name

