from model import make_suggestions, processing_data
from model import settings
import numpy as np
import pandas as pd


def run(start_date, end_date, num_days_left, function, punish_level = 0, distance = True):

    tau_df = pd.DataFrame({})
    for site in settings.telescopes:
        tau_df[site] = list(- processing_data.day_reward(site, start_date, end_date, \
                                           settings.dict_schedule[settings.telescopes[0]][0],
                                           settings.dict_schedule[settings.telescopes[0]][1],punish_level=0).value)

    tau_df.index = processing_data.day_reward(settings.telescopes[0], start_date, end_date, \
                                           settings.dict_schedule[settings.telescopes[0]][0],
                                           settings.dict_schedule[settings.telescopes[0]][1],punish_level=0).index

    if num_days_left <= 0:
        return None, None, None, None, tau_df, None, None
    else:
        should_trigger, selected_future_days, confidence_level, each_day_score, second_optimal, second_optimal_prob = function(start_date, end_date, num_days_left, punish_level, distance)
        return should_trigger, sorted(selected_future_days), confidence_level, each_day_score, tau_df, second_optimal, second_optimal_prob 
if __name__ == '__main__':
    print(run(settings.start_date, settings.end_date, settings.days_left, make_suggestions.decision_making_sampling, 0, True))
