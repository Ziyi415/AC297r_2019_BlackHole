import pandas as pd
import numpy as np

### Data Path
# data_path = "/Users/susanaxu/Desktop/src/forecast_data"
data_path = "forecast_data"

### Window Information
start_date = "2019-10-25"
end_date = "2019-11-09"
days_left = 5

# change the name of each telescopes here
telescopes = ['12-meter', 'alma', 'apex', 'aste', 'iram', 'jcmt', 'lmt', 'sma', 'smt', 'spt']

# change the weight of each telescopes here
# each entry should correspond to the telescope
weights = [144.0, 5329.0, 144.0, 100.0, 900.0, 225.0, 1056.25, 216.09, 100.0, 36.0]

# change the scheduling hour for each telescope here
# each entry should correspond to the telescope
# [0, 23] means that the telescope will operate the whole day
# [3, 13] means that the telescope will operate from 3 AM to 1 PM
# defaulted to follow the settings in the scheduling file of April 24, 2018
schedules = [(0, 23), (3, 13), (3, 15), (0, 23), (0, 23), (10, 16), (6, 16), (10, 16), (8, 16), (3, 15)]

# combine telescope name with hourly schedule and weights
dict_schedule = dict(zip(telescopes, schedules))
dict_weight = dict(zip(telescopes, weights))

# change the baseline matrix
baseline_lengths = np.array([[0.0, 7.683, 7.681, 7.682, 9.317, 4.553, 2.029, 4.553, 0.182, 13.551], [7.683, 0.0, 0.002, 0.007, 9.478, 9.448, 5.469, 9.448, 7.176, 7.041], [7.681, 0.002, 0.0, 0.007, 9.477, 9.447, 5.467, 9.447, 7.174, 7.043], [7.682, 0.007, 0.007, 0.0, 9.47, 10.63, 5.662, 10.63, 7.634, 7.448], [9.317, 9.478, 9.477, 9.47, 0.0, 13.036, 9.078, 13.036, 9.139, 14.12], [4.553, 9.448, 9.447, 10.63, 13.036, 0.0, 5.854, 0.0, 4.627, 10.416], [2.029, 5.469, 5.467, 5.662, 9.078, 5.854, 0.0, 5.854, 1.964, 10.363], [4.553, 9.448, 9.447, 10.63, 13.036, 0.0, 5.854, 0.0, 4.627, 10.416], [0.182, 7.176, 7.174, 7.634, 9.139, 4.627, 1.964, 4.627, 0.0, 11.166], [13.551, 7.041, 7.043, 7.448, 14.12, 10.416, 10.363, 10.416, 11.166, 0.0]])

# For training/validation purpose
training = False
available_data_start = "2019-10-25" # all data for this date must be available (00 06 12 18 oclock)
available_data_end = "2019-11-30"