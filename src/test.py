from model import make_suggestions, processing_data, read_data
from model import settings
import pandas as pd
from importlib import reload


def run(start_date, end_date, num_days_left, function, databook, std_dict, punish_level=0, distance=True):
    reload(settings)
    # Get the dataframe of tau225 forecast for all sites
    tau_df = pd.DataFrame({})
    for site in settings.telescopes:
        tau_df[site] = list(- processing_data.day_reward(site, start_date, end_date, \
                                                         settings.dict_schedule[settings.telescopes[0]][0],
                                                         settings.dict_schedule[settings.telescopes[0]][1], databook,
                                                         std_dict, punish_level=0).value)

    tau_df.index = processing_data.day_reward(settings.telescopes[0], start_date, end_date, \
                                              settings.dict_schedule[settings.telescopes[0]][0],
                                              settings.dict_schedule[settings.telescopes[0]][1], databook, std_dict,
                                              punish_level=0).index

    if num_days_left <= 0:
        return None, None, None, None, tau_df, None, None
    else:
        # Make a path suggestion
        should_trigger, selected_future_days, confidence_level, each_day_score, second_optimal, second_optimal_prob = function(
            start_date, end_date, databook, std_dict, num_days_left, punish_level, distance)
        return should_trigger, sorted(
            selected_future_days), confidence_level, each_day_score, tau_df, second_optimal, second_optimal_prob




if __name__ == '__main__':
    databook, std_dict = read_data.run_read_data(settings.start_date, settings.end_date)
    print(run(settings.start_date, settings.end_date, settings.days_left, make_suggestions.decision_making_sampling, databook, std_dict, 0, True))
