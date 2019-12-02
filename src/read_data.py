import settings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

### inputs from GUI
start_date = '2019-10-25'
end_date = '2019-11-03'
days_left = 5

### build databook
# data collection start time and end time
# this is different than the observation start day and end day
starttime = datetime(2019,10,24,6)
endtime = datetime(2019,12,1,0)# not included
# Input from GUI
data_path = "../notebooks/data/"

def build_databook(starttime, endtime, data_path):
    timestamps = np.arange(starttime, endtime,
                           timedelta(hours=6)).astype(datetime)
    databook = {}
    for site in settings.telescopes:
        databook[site] = dict.fromkeys(timestamps)

    for site in settings.telescopes:
        for t in timestamps:
            filepath = data_path + site + "/" + t.strftime("%Y%m%d_%H:%M:%S")
            try:
                df = pd.read_csv(filepath, delim_whitespace= True, skiprows= 1, header = None)
                df.columns = ["date", "tau225", "Tb[k]", "pwv[mm]", "lwp[kg*m^-2]","iwp[kg*m^-2]","o3[DU]"]
                df['date'] = pd.to_datetime(df['date'], format = "%Y%m%d_%H:%M:%S")
                databook[site][t] = df
            except FileNotFoundError:
                databook[site][t] = None
    return databook

databook = build_databook(starttime, endtime, data_path)

# print(settings.telescopes[0],timestamps[1], databook[settings.telescopes[0]][timestamps[1]].head())

### build std_dict
std_dict = {}
for site in settings.telescopes:
    data_telescope = databook[site]
    df_tau225 = pd.concat([data_telescope[t].set_index('date')['tau225'] for t in data_telescope if data_telescope[t] is not None], axis=1)
    df_tau225.columns = [t for t in data_telescope if data_telescope[t] is not None]

    # use df_mask to record the number of days forward (index - col) for each prediction
    df_mask = pd.DataFrame(index=df_tau225.index, columns=df_tau225.columns)
    for col in df_tau225.columns:
        df_mask[col] = (df_tau225.index - col).days

    # get 'true' tau225 value, which is the closest prediction within a day
    true_tau225 = pd.Series(index=df_tau225.index)
    for idx in df_tau225.index:
        values = df_tau225.loc[idx]
        true_tau225[idx] = values.values[~values.isna()][-1]

    # compute standard error v.s. # days forward
    df_diff = (df_tau225.T - true_tau225).T
    std = []
    for i in range(1, df_mask.max().max() + 1):
        std.append((np.nanmean(df_diff[df_mask == i].values ** 2)) ** (1 / 2))

    std_dict[site] = std[:10]

print("read_data")