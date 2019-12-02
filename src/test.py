from model import make_suggestions
from model import settings
import numpy as np


def main(start_date, end_date, num_days_left, function, punish_level = 0, distance = True):

    if num_days_left <= 0:
        return None, None, None
    else:
        should_trigger, selected_future_days, confidence_level = function(start_date, end_date, num_days_left, punish_level, distance)
        return should_trigger, selected_future_days, confidence_level

if __name__ == '__main__':
    print(main(settings.start_date, settings.end_date, settings.days_left, make_suggestions.decision_making_further_std_punishment, 0, settings.distance))
