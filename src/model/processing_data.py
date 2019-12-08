from model import settings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta





def day_reward(telescope_name, day_current_str, end_day_str, start_time, end_time, databook, std_dict,\
               use_as_evaluate=False, time_std=False, further_std=False, punish_level=1, sampled=False):
    '''
    For the specified telescope, return a dataframe with two columns.
    The first column tells the day in the day window between
        day_current_str and end_day_str (inclusive).
    The second column tells the average predicted tao225 given the day and the time window between
        start_time and end_time (inclusive).

    '''

    day_current = datetime.strptime(day_current_str,"%Y-%m-%d")
    day_end = datetime.strptime(end_day_str,"%Y-%m-%d") + timedelta(days=1)

    if not use_as_evaluate:
        mask = [t < day_current for t in databook[telescope_name]]
        t_valid = np.array([t for t in databook[telescope_name]])[mask]
        df_all = pd.concat([databook[telescope_name][t] for t in t_valid], axis=0)
    else:
        df_all = pd.concat([databook[telescope_name][t] for t in databook[telescope_name]], axis=0)

    # day and time filter
    df_all = df_all[(df_all.date >= day_current) & (df_all.date < day_end)]
    df_all['day'] = df_all.date.apply(lambda x: str(x).split(' ')[0])
    df_all['time'] = df_all.date.apply(lambda x: int(str(x).split(' ')[1][0:2]))
    df_all = df_all[(df_all.time >= int(start_time)) & (df_all.time <= int(end_time))]

    # calculate the day reward
    df_tau_all = df_all.groupby('date').agg({'tau225': lambda x: list(x)}).reset_index()
    df_tau_all['day'] = df_tau_all.date.apply(lambda x: str(x).split(' ')[0])

    df_tau_all['latest'] = df_tau_all['tau225'].apply(lambda x: - x[-1])
    df_tau_all['mean'] = df_tau_all['tau225'].apply(lambda x: - np.mean(x))
    # df_tau_all['std'] = df_tau_all['tau225'].apply(lambda x: np.std(x))
    df_tau_all['rmse'] = df_tau_all['tau225'].apply(lambda x: np.sqrt(np.mean((np.array(x) - x[-1])**2)))

    if sampled:
        sample_df = pd.DataFrame(
            np.random.normal(df_tau_all['latest'], df_tau_all['rmse'], (100, len(df_tau_all))).T)
        df_tau_all = pd.concat([df_tau_all[['date', 'day']], sample_df], axis=1)
        df_tau_day = pd.DataFrame(df_tau_all.groupby('day').mean())

    elif time_std:
        df_tau_day = pd.DataFrame(df_tau_all.groupby('day').apply(
            lambda x: np.mean(x['latest'] * np.exp(punish_level * x['rmse'])))) 
        df_tau_day.columns = ['value']

    else:
        df_tau_day = pd.DataFrame(df_tau_all.groupby('day')['latest'].mean())
        df_tau_day.columns = ['value']

        if further_std:
            df_tau_day['value'] = df_tau_day['value'].values * np.exp(
                np.array(std_dict[telescope_name][:len(df_tau_day)]) * punish_level)

    return df_tau_day


def all_day_reward(day_current_str, end_day_str, databook, std_dict, time_std=False, further_std=False, punish_level=1, sampled=False, distance = True, use_as_evaluate=False):
    """
    calculate F(D) for D in range(day_current_str, end_day_str)
    taking in every single telescope we currently have
    weighted their f reward values
    based on area_i/total_area
    """

    if distance and not sampled:
        # set up a dataframe
        telescopes_day_reward = day_reward(settings.telescopes[0], day_current_str, end_day_str,
                                           settings.dict_schedule[settings.telescopes[0]][0],
                                           settings.dict_schedule[settings.telescopes[0]][1],
                                           databook, std_dict,
                                           time_std=time_std, further_std=further_std, punish_level=punish_level,
                                           sampled=sampled, use_as_evaluate=use_as_evaluate) \
                                * settings.dict_weight[settings.telescopes[0]]
        # set up a matrix f.T
        f_T = telescopes_day_reward.values

        # fill up the matrix
        for i in settings.telescopes[1:]:
            new_telescope = day_reward(i, day_current_str, end_day_str,
                                        settings.dict_schedule[i][0], settings.dict_schedule[i][1], databook, std_dict,
                                        time_std=time_std, further_std=further_std, punish_level=punish_level,
                                        sampled=sampled, use_as_evaluate=use_as_evaluate) \
                                     * settings.dict_weight[i]
            f_T = np.hstack([f_T, new_telescope.values])
        # calculate the number of telescopes
        num_tele = len(settings.telescopes)

        # calculate f.T @ D @ 1
        # f.T is d * n, d is number of days, n is number of telescopes
        # D is n * n, element-wise reciprocal of baseline length matrix
        # 1 is n * 1, a column vector of 1's
        inv_D = settings.baseline_lengths * 1.0
        inv_D[inv_D != 0] = 1 / inv_D[inv_D != 0]
        F = f_T @ inv_D @ np.array([[1]*num_tele]).T

        # replace values in the dataframe with indices as days
        telescopes_day_reward['value'] = F
        F = telescopes_day_reward / sum(settings.weights)

    if distance and sampled:
        # for the sampling method
        # the returned dataframe will be in shape d * 100, d is number of days, 100 is the number of samples we take

        # run for the first telescope to get number of days
        new_telescope = day_reward(settings.telescopes[0], day_current_str, end_day_str, \
                                           settings.dict_schedule[settings.telescopes[0]][0],
                                           settings.dict_schedule[settings.telescopes[0]][1], databook, std_dict,
                                           time_std=time_std, further_std=further_std, punish_level=punish_level,
                                           sampled=sampled, use_as_evaluate=use_as_evaluate) \
                                * settings.dict_weight[settings.telescopes[0]]

        # calculate the number of telescopes
        num_tele = len(settings.telescopes)

        # record sampled values
        sampled_f = np.zeros((num_tele, new_telescope.values.shape[0], new_telescope.values.shape[1]))
        index = 0
        sampled_f[index] = new_telescope.values


        for i in settings.telescopes[1:]:
            index += 1
            new_telescope = day_reward(i, day_current_str, end_day_str, \
                       settings.dict_schedule[i][0], settings.dict_schedule[i][1], databook, std_dict,
                       time_std=time_std, further_std=further_std, punish_level=punish_level,
                       sampled=sampled, use_as_evaluate=use_as_evaluate) * settings.dict_weight[i]
            sampled_f[index] = new_telescope.values



        # slicing each set of sample
        for j in range(100): #because we sampled 100 tao-225 for each telescope on each day
            # calculate f.T @ D @ 1
            # f.T is d * n, d is number of days, n is number of telescopes
            # D is n * n, element-wise reciprocal of baseline length matrix
            # 1 is n * 1, a column vector of 1's
            f_T = np.hstack([sampled_f[k, :, j].reshape(-1,1) for k in range(num_tele)])
            inv_D = settings.baseline_lengths * 1.0
            inv_D[inv_D != 0] = 1 / inv_D[inv_D != 0]
            F = f_T @ inv_D @ np.array([[1] * num_tele]).T
            # replace values in the dataframe
            new_telescope.loc[:, j] = F
        F = new_telescope / sum(settings.weights)

    else:
        # set up a dataframe
        telescopes_day_reward = day_reward(settings.telescopes[0], day_current_str, end_day_str, \
                                           settings.dict_schedule[settings.telescopes[0]][0], settings.dict_schedule[settings.telescopes[0]][1], \
                                           databook, std_dict,
                                           time_std=time_std, further_std=further_std, punish_level=punish_level,
                                           sampled=sampled, use_as_evaluate=use_as_evaluate) \
                                * settings.dict_weight[settings.telescopes[0]]

        # fill up the dataframe
        for i in settings.telescopes[1:]:
            telescopes_day_reward += day_reward(i, day_current_str, end_day_str, \
                                                settings.dict_schedule[i][0], settings.dict_schedule[i][1],
                                                databook, std_dict,
                                                time_std=time_std, further_std=further_std, punish_level=punish_level,
                                                sampled=sampled, use_as_evaluate=use_as_evaluate) \
                                     * settings.dict_weight[i]
        F = telescopes_day_reward / sum(settings.weights)

    return F

if __name__ == '__main__':
    print("processing_data")