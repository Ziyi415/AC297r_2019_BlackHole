import make_suggestions
import read_data
import numpy as np


def main(start_date, end_date, num_days_left, function, punish_level = 0):

    if num_days_left <= 0:
        return None, None, None
    else:
        should_trigger, selected_future_days, confidence_level = function(start_date, end_date, num_days_left, punish_level)
        return should_trigger, selected_future_days, confidence_level

print(main(read_data.start_date, read_data.end_date, read_data.days_left, make_suggestions.decision_making_sampling, 0))
print('decision_making_sampling')
