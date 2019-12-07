from model import make_suggestions, processing_data
from model import settings
import numpy as np


def main(start_date, end_date, num_days_left, function, punish_level = 0, distance = True):

    tau_dict = {}
    for site in settings.telescopes:
        tau_dict[site] = - processing_data.day_reward(site, start_date, end_date, \
                                           settings.dict_schedule[settings.telescopes[0]][0],
                                           settings.dict_schedule[settings.telescopes[0]][1],punish_level=0)

    if num_days_left <= 0:
        return None, None, None, None, tau_dict
    else:
        should_trigger, selected_future_days, confidence_level, each_day_score= function(start_date, end_date, num_days_left, punish_level, distance)
        return should_trigger, selected_future_days, confidence_level, each_day_score, tau_dict

if __name__ == '__main__':
    print(main(settings.start_date, settings.end_date, settings.days_left, make_suggestions.decision_making_single_punishment, 0, settings.distance))
