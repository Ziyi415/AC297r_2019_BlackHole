import numpy as np
from model import processing_data


def decision_making_single_punishment(day_current_str, end_day_str, days_to_trigger, punish_level=0, distance = True, use_as_evaluate=False):
    # day_current_str: YYYY-MM-DD (str) (included)
    # end_day_str: YYYY-MM-DD (str) (included)
    # days_to_trigger: days to trigger (int)
    # days_to_trigger: days to trigger (int)
    each_day_reward = processing_data.all_day_reward(day_current_str, end_day_str, distance = True, use_as_evaluate=use_as_evaluate)

    # inflate the values on each day
    scores = np.array([n * ((1 + punish_level) ** i) for i, n in enumerate(each_day_reward['value'])])

    # select the 'days_to_trigger' number of days having maximum reward values
    selected_days = np.array(each_day_reward.index)[np.argsort(scores)[-1:-days_to_trigger - 1:-1]]

    if day_current_str in selected_days:
        # print('We suggest triggering on today {}'.format(day_current_str))
        output = True
    else:
        # print('We DO NOT suggest triggering on today {}'.format(day_current_str))
        output = False
    # print('And we suggest to trigger by the following sequence: {}'.format(np.array(sorted(selected_days))))
    # dic = dict(zip(each_day_reward.index, a))
    # print('The discounted reward values for all the future days are ', dic)
    return output, selected_days, None, scores, None, None


def decision_making_further_std_punishment(day_current_str, end_day_str, days_to_trigger, punish_level=0, distance = True, use_as_evaluate=False):
    # day_current_str: YYYY-MM-DD (str) (included)
    # end_day_str: YYYY-MM-DD (str) (included)
    # days_to_trigger: days to trigger (int)
    each_day_reward = processing_data.all_day_reward(day_current_str, end_day_str, further_std=True, punish_level=punish_level, distance = True, use_as_evaluate=use_as_evaluate)

    # select the 'days_to_trigger' number of days having maximum reward values
    selected_days = each_day_reward.sort_values(by='value', ascending=False)[:days_to_trigger].index

    if day_current_str in selected_days:
        # print('We suggest triggering on today {}'.format(day_current_str))
        output = True
    else:
        # print('We DO NOT suggest triggering on today {}'.format(day_current_str))
        output = False
    # print('And we suggest to trigger by the following sequence: {}'.format(np.array(sorted(selected_days))))
    # dic = each_day_reward.to_dict()['value']
    # print('The discounted reward values for all the future days are ', dic)
    return output, selected_days, None, each_day_reward, None, None


def decision_making_time_std_punishment(day_current_str, end_day_str, days_to_trigger, punish_level=0, distance = True, use_as_evaluate=False):
    # day_current_str: YYYY-MM-DD (str) (included)
    # end_day_str: YYYY-MM-DD (str) (included)
    # days_to_trigger: days to trigger (int)
    each_day_reward = processing_data.all_day_reward(day_current_str, end_day_str, time_std=True, punish_level=punish_level, distance = True, use_as_evaluate=use_as_evaluate)

    # select the 'days_to_trigger' number of days having maximum reward values
    selected_days = each_day_reward.sort_values(by='value', ascending=False)[:days_to_trigger].index

    if day_current_str in selected_days:
        # print('We suggest triggering on today {}'.format(day_current_str))
        output = True
    else:
        # print('We DO NOT suggest triggering on today {}'.format(day_current_str))
        output = False
    # print('And we suggest to trigger by the following sequence: {}'.format(np.array(sorted(selected_days))))
    # dic = each_day_reward.to_dict()['value']
    # print('The discounted reward values for all the future days are ', dic)
    return output, selected_days, None, each_day_reward, None, None


def decision_making_sampling(day_current_str, end_day_str, days_to_trigger, punish_level=0, distance = True, use_as_evaluate=False):
    each_day_reward = processing_data.all_day_reward(day_current_str, end_day_str, sampled=True, punish_level = punish_level, distance = True, use_as_evaluate=use_as_evaluate)
    num_samples = each_day_reward.shape[-1]

    threshold_value = np.sort(np.array(each_day_reward).T, axis=1)[:, -days_to_trigger]

    mask = np.array(each_day_reward) >= threshold_value
    # prob_current_day = np.sum(mask, axis = 1)[0]/num_samples

    # work on suggested path
    index_matrix = np.tile(np.array(each_day_reward.index), (num_samples, 1))
    suggested_path_matrix = index_matrix[mask.T].reshape(-1, days_to_trigger)

    # this part can be improved
    path_dict = {}
    for i in suggested_path_matrix:
        if str(i) not in path_dict:
            path_dict[str(i)] = 0
        else:
            path_dict[str(i)] += 1

    suggested_path = max(path_dict, key=path_dict.get)
    prob_suggested_path = path_dict[suggested_path] / num_samples
    if day_current_str == suggested_path.split("'")[1]:
        # print('We suggest triggering on today {} (Confidence Level {})'.format(day_current_str, prob_current_day))
        output = True
    else:
        # print('We DO NOT suggest triggering on today {} (Confidence Level {})'.format(day_current_str,
        #                                                                               1 - prob_current_day))
        output = False
    # print('The suggested path is ' + suggested_path + ' (Confidence Level {})'.format(prob_suggested_path))
    suggested_path = list(suggested_path.split("'"))[1::2] 
    try: 
        second_optimal = sorted(path_dict.items(), key=lambda kv: kv[1])[-2][0]
        prob_second_path = path_dict[second_optimal] / num_samples
        second_optimal = list(second_optimal.split("'"))[1::2] 
    except:
        second_optimal = None
        prob_second_path = None

    return output, suggested_path, prob_suggested_path, each_day_reward, second_optimal, prob_second_path

print("make_suggestions")