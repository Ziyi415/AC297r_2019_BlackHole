
import numpy as np
def writeSettings(data_path, start_date, end_date, days_left, telescope_name, telescope_weight, telescope_schedule, baseline_matrix):
    f = open('model/settings.py', 'w+')
    file_txt = [
        'import pandas as pd\nimport numpy as np',
        '\n\n### Data Path',
        '\ndata_path = "{}"'.format(data_path),
        '\n\n### Window Information',
        '\nstart_date = "{}"'.format(start_date),
        '\nend_date = "{}"'.format(end_date),
        '\ndays_left = {}'.format(days_left),
        '\n\n# change the name of each telescopes here'
        '\ntelescopes = {}'.format(telescope_name),
        '\n\n# change the weight of each telescopes here\n# each entry should correspond to the telescope',
        '\nweights = {}'.format(telescope_weight),
        '\n\n# change the scheduling hour for each telescope here\n# each entry should correspond to the telescope\n# [0, 23] means that the telescope will operate the whole day\n# [3, 13] means that the telescope will operate from 3 AM to 1 PM\n# defaulted to follow the settings in the scheduling file of April 24, 2018', 
        '\nschedules = {}'.format(telescope_schedule),
        '\n\n# combine telescope name with hourly schedule and weights',
        '\ndict_schedule = dict(zip(telescopes, schedules))\ndict_weight = dict(zip(telescopes, weights))',
        '\n\n# change the baseline matrix',
        '\nbaseline_lengths = np.array({})'.format([list(i) for i in baseline_matrix])
    ]

    for i in file_txt:
        f.write(i)
    f.close()

if __name__ == '__main__':
    data_path = "../notebooks/data/"
    start_date = '2019-10-25'
    end_date = '2019-11-03'
    days_left = 5
    telescope_name = ['12-meter', 'alma', 'apex', 'aste', 'iram', 'jcmt', 'lmt', 'sma', 'smt', 'spt']
    telescope_weight = [12**2, 73**2, 12**2, 10**2, 30**2, 15**2, 32.5**2, 14.7**2, 10**2, 6**2]
    telescope_schedule = [[0, 23], [3, 13], [3, 15], [0, 23], [0, 23], [10, 16], [6, 16], [10, 16], [8, 16], [3, 15]]
    baseline_matrix = np.array([[    0,     2,  7041,  5469,  7176,  9448,  9448],
       [    2,     0,  7043,  5467,  7174,  9447,  9447],
       [ 7041,  7043,     0, 10363, 11166, 10416, 10416],
       [ 5469,  5467, 10363,     0,  1964,  5854,  5854],
       [ 7176,  7174, 11166,  1964,     0,  4627,  4627],
       [ 9448,  9447, 10416,  5854,  4627,     0,     0],
       [ 9448,  9447, 10416,  5854,  4627,     0,     0]])
    writeSettings(data_path, start_date, end_date, days_left, telescope_name, telescope_weight, telescope_schedule, baseline_matrix)
