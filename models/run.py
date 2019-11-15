import make_suggestions
import processing_data
import read_data
import numpy as np

def main(start_date, end_date, num_days_left, function, punish_level):

    if num_days_left <= 0:
        return None, None
    else:
        should_trigger, selected_future_days = function(start_date, end_date, num_days_left, punish_level)
        return should_trigger, selected_future_days


