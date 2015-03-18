import pandas as pd
import numpy as np
from dtw import dtw

from matplotlib import pyplot as plt


ppt_colname = 'ppt'
event_type_colname = 'event_type'
category_colname = 'category'
x_colname = 'xpos'
y_colname = 'ypos'
repetition_colname = 'repetition'

def subset(data, colname, value):
    formula = data[colname] == value
    return data[formula]

def get_participant_data(data, participant_num):
    return data[data[ppt_colname] == participant_num]

def remove_cue_event(data):
    return data[data['event_type'] != 'CUE_ENTER_ZONE']

def keep_seq(data):
    return data[data['category'] == 'Seq']

def get_matrix_intra(ppt, category_order=['Seq', 'Foil1', 'Foil2']):
    summary = trace_data.groupby(category_colname).agg({repetition_colname: np.max})
    max_repetitions = summary.to_dict()[repetition_colname]

    n = sum(max_repetitions.values())
    mat = np.zeros((n, n))

    for cat1_index, cat1_name in enumerate(category_order):
        data_cat1 = ppt[ppt[category_colname] == cat1_name]
        for cat2_index, cat2_name in enumerate(category_order[cat1_index::]):
            data_cat2 = ppt[ppt[category_colname] == cat2_name]

            same_cats = cat1_name == cat2_name
            for repetition1 in range(1, max_repetitions[cat1_name] + (not same_cats)):
                data_repetition1 = data_cat1[data_cat1[repetition_colname] == repetition1]
                for repetition2 in range(repetition1 + 1 if same_cats else 1, max_repetitions[cat2_name] + 1):
                    data_repetition2 = data_cat2[data_cat2[repetition_colname] == repetition2]

                    dist, cost, path = dtw(data_repetition1[x_colname], data_repetition2[x_colname])
                    mat[cat1_index*max_repetitions[cat1_name] + repetition1 - 1, 
                        (cat1_index + cat2_index)*max_repetitions[cat2_name] + repetition2 - 1] = dist

    return mat

def get_matrix_inter(data, participants):
    summary = data.groupby(ppt_colname).agg({repetition_colname: np.max})
    max_repetitions = summary.to_dict()[repetition_colname]

    n = sum(max_repetitions.values())
    mat = np.zeros((n, n))

    for ppt1_index, ppt1_name in enumerate(participants):
        data_ppt1 = data[data[ppt_colname] == ppt1_name]
        for ppt2_index, ppt2_name in enumerate(participants[ppt1_index::]):
            data_ppt2 = data[data[ppt_colname] == ppt2_name]

            same_ppts = ppt1_name == ppt2_name
            for repetition1 in range(1, max_repetitions[ppt1_name] + (not same_ppts)):
                data_repetition1 = data_ppt1[data_ppt1[repetition_colname] == repetition1]
                for repetition2 in range(repetition1 + 1 if same_ppts else 1, max_repetitions[ppt2_name] + 1):
                    data_repetition2 = data_ppt2[data_ppt2[repetition_colname] == repetition2]

                    dist, cost, path = dtw(data_repetition1[x_colname], data_repetition2[x_colname])
                    mat[sum(max_repetitions.values()[:ppt1_index]) + repetition1 - 1, 
                        sum(max_repetitions.values()[:ppt1_index + ppt2_index]) + repetition2 - 1] = dist
            
            plot_matrix(mat, 'imgs/all-inter-seq-dist.png')

    return mat

def plot_matrix(mat, save_filename=None):
    if save_filename is not None:
        fig = plt.figure()

    plt.matshow(mat)
    plt.colorbar()
    
    if save_filename is None:
        plt.show()
    else:
        print('Saving file [%s]' % save_filename)
        plt.savefig(save_filename)
        plt.close(fig)

def get_ordered_participants(data):
    cue_created = data[
        (data['event_type'] == 'CUE_ENTER_ZONE') & \
        (data['repetition'] == 1)
    ]
    grouped = cue_created.groupby(ppt_colname)
    l = [(tuple(data_pt['event_value']), pt) for pt, data_pt in grouped]
    
    d = dict()
    for k, v in l:
        d.setdefault(hash(k), list()).append(v)
    
    return d.values()


trace_data = pd.read_csv('data/test_traces.csv')

def get_participant_dist_intra(trace_data=trace_data):
    participants = trace_data[ppt_colname].unique()
    seq_trace_data = remove_cue_event(trace_data)
    for participant in participants:
        ppt = get_participant_data(seq_trace_data, participant)
        mat = get_matrix_intra(ppt)
        mat = mat + mat.T

        ppt_id = str(int(participant*10000))[0:5]
        plot_matrix(mat, 'imgs/all-dist-%s.png' % ppt_id)
        np.savetxt("data/all-dist-%s.csv" % ppt_id, mat, delimiter=",")

def get_participant_dist_inter(trace_data=trace_data):
    data = trace_data[trace_data[category_colname] == 'Seq']

    participants_grouped = get_ordered_participants(data)
    participants = reduce(lambda x, y: x + y, participants_grouped, [])
    participants.remove(9640.0) # removing bad player
    print participants

    seq_trace_data = remove_cue_event(data)
    mat = get_matrix_inter(seq_trace_data, participants)
    mat = mat + mat.T

    plot_matrix(mat, 'imgs/all-inter-seq-dist.png')
    np.savetxt("data/all-inter-seq-dist.csv", mat, delimiter=",")

