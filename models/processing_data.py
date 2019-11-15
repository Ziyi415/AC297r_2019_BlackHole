import read_data
import numpy as np

def day_reward(telescope_name, day_current_str, end_day_str, start_time, end_time, \
               use_as_evaluate=False, time_std=False, furthure_std=False, punish_level=1, sampled=False):
    '''
    For the specified telescope, return a dataframe with two columns.
    The first column tells the day in the day window between
        day_current_str and end_day_str (inclusive).
    The second column tells the average predicted tao225 given the day and the time window between
        start_time and end_time (inclusive).

    '''
    split_day_current = day_current_str.split('-')
    split_day_end = end_day_str.split('-')  # include this day

    day_current = datetime(int(split_day_current[0]), int(split_day_current[1]), int(split_day_current[2]), 0)
    day_end = datetime(int(split_day_end[0]), int(split_day_end[1]), int(split_day_end[2]) + 1, 0)

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
    df_tau_all['std'] = df_tau_all['tau225'].apply(lambda x: np.std(x))

    if sampled:
        sample_df = pd.DataFrame(
            np.random.normal(df_tau_all['latest'], df_tau_all['mse'], (100, len(df_tau_all))).T)  # todo
        df_tau_all = pd.concat([df_tau_all[['date', 'day']], sample_df], axis=1)
        df_tau_day = pd.DataFrame(df_tau_all.groupby('day').mean())

    elif time_std:
        df_tau_day = pd.DataFrame(df_tau_all.groupby('day').apply(
            lambda x: np.mean(x['latest'] * np.exp(punish_level * x['mse']))))  # should be mse
        df_tau_day.columns = ['value']

    else:
        df_tau_day = pd.DataFrame(df_tau_all.groupby('day')['latest'].mean())
        df_tau_day.columns = ['value']

        if furthure_std:
            df_tau_day['value'] = df_tau_day['value'].values * np.exp(
                np.array(std_dict[telescope_name][:len(df_tau_day)]) * punish_level)

    return df_tau_day

def all_day_reward(day_current_str, end_day_str, time_std = False, furthure_std = False, punish_level = 1, sampled = False):
    """
    calculate F(D) for D in range(day_current_str, end_day_str)
    taking in every single telescope we currently have
    weighted their f reward values
    based on area_i/total_area
    """
    # set up a dataframe
    telescopes_day_reward = day_reward(telescopes[0], day_current_str, end_day_str, \
                                       dict_schedule[telescopes[0]][0], dict_schedule[telescopes[0]][1], \
                                       time_std = time_std, furthure_std = furthure_std, punish_level = punish_level, sampled = sampled) \
                                       * dict_weight[telescopes[0]]
    #
    for i in telescopes[1:]:
        telescopes_day_reward += day_reward(i, day_current_str, end_day_str, \
                                            dict_schedule[i][0], dict_schedule[i][1], \
                                            time_std = time_std, furthure_std = furthure_std,  punish_level = punish_level, sampled = sampled)\
                                            * dict_weight[i]
    return telescopes_day_reward / sum(weight_telescope)


whole_time_window = all_day_reward(read_data.start_date, read_data.end_date)
days = np.array(whole_time_window.index)