import numpy as np

### Inputs from GUI

# change the name of each telescopes here
# must be the same as data folder name
telescopes = ['12-meter', 'alma', 'apex', 'aste', 'iram', 'jcmt', 'lmt', 'sma', 'smt', 'spt']

# change the weight of each telescopes here
# each entry should correspond to the telescope
weights = [12**2, 73**2, 12**2, 10**2, 30**2, 15**2, 32.5**2, 14.7**2, 10**2, 6**2]  # defaulted to be radius squared

# change the scheduling hour for each telescope here
# each entry should correspond to the telescope
# [0, 23] means that the telescope will operate the whole day
# [3, 13] means that the telescope will operate from 3 AM to 1 PM
# defaulted to follow the settings in the scheduling file of April 24, 2018
schedules = [[0, 23], [3, 13], [3, 15], [0, 23], [0, 23], [10, 16], [6, 16], [10, 16], [8, 16], [3, 15]]

# combine telescope name with hourly schedule and weights
dict_schedule = dict(zip(telescopes, schedules))
dict_weight = dict(zip(telescopes, weights))

# change the baseline matrix
# TODO
# baseline_lengths = [[0, 2, 8624, 7041, 5469, 7176, ...]]

print('settings')