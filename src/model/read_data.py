from model import settings
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def create_databook(starttime, endtime):
    timestamps = np.arange(starttime, endtime,
                        timedelta(hours=6)).astype(datetime)
    databook = {}
    for site in settings.telescopes:
        databook[site] = dict.fromkeys(timestamps)

    for site in settings.telescopes:
        for t in timestamps:
            # Input from GUI
            filepath = settings.data_path + "/"  + site + "/" + t.strftime("%Y%m%d_%H:%M:%S")
            try:
                df = pd.read_csv(filepath, delim_whitespace= True, skiprows= 1, header = None)
                df.columns = ["date", "tau225", "Tb[k]", "pwv[mm]", "lwp[kg*m^-2]","iwp[kg*m^-2]","o3[DU]"]
                df['date'] = pd.to_datetime(df['date'], format = "%Y%m%d_%H:%M:%S")
                databook[site][t] = df
            except FileNotFoundError:
                databook[site][t] = None
    return databook



def run_read_data(start_date, end_date):
    ### build databook
    # data collection start time and end time
    # this is different than the observation start day and end day
    starttime = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=16)
    endtime = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

    if settings.training:
        databook = create_databook(datetime.strptime(settings.available_data_start, "%Y-%m-%d"), \
                                             datetime.strptime(settings.available_data_end, "%Y-%m-%d"))
    else:
        databook = create_databook(starttime, endtime)

    if settings.training:
        ### build std_dict - this is the variance only related to # days in the future that the weather model predict
        std_dict = {}
        for site in settings.telescopes:
            data_telescope = databook[site]
            df_tau225 = pd.concat([data_telescope[t].set_index('date')['tau225'] for t in data_telescope if
                                   data_telescope[t] is not None], axis=1)
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

            std_dict[site] = std[:16]

    else:
        std_dict = {'12-meter': [0.12460340226659794,
                                 0.14027262850095598,
                                 0.17601987358866908,
                                 0.22617363103716592,
                                 0.27667432390741464,
                                 0.34010743654752035,
                                 0.4151433055140587,
                                 0.41530544534999725,
                                 0.4092011436901557,
                                 0.3967737426906885,
                                 0.4428971051967838,
                                 0.44714575331198797,
                                 0.48445162458109975,
                                 0.4712027072757511,
                                 0.4775881736783054,
                                 0.45465792082534395],
                    'alma': [0.023672613182526198,
                             0.032085879096746726,
                             0.03979667725426756,
                             0.047860966843364626,
                             0.05736262847677088,
                             0.07566834650092459,
                             0.08702386134184176,
                             0.09139674341047788,
                             0.09384965540417152,
                             0.09292825665937893,
                             0.0965861897581782,
                             0.09023731398233877,
                             0.09303510231250975,
                             0.09601842272110242,
                             0.10652398211021769,
                             0.11281488735201216],
                    'apex': [0.023725445009116646,
                             0.03211327274617207,
                             0.03984439045700136,
                             0.0480264917802912,
                             0.05735098941400619,
                             0.07589225643844581,
                             0.08712529666023197,
                             0.09140873959454886,
                             0.09389740237481953,
                             0.09297306345657327,
                             0.0966128676650958,
                             0.09029061802138685,
                             0.09305473845260728,
                             0.09605586623606574,
                             0.106527374660924,
                             0.11281339903057377],
                    'aste': [0.025887110415262468,
                             0.03545246173624117,
                             0.04519372350819946,
                             0.05338445049468958,
                             0.06337664240524105,
                             0.0824530653668525,
                             0.09610055422695298,
                             0.10161452036901931,
                             0.10529440454487252,
                             0.1051288197104957,
                             0.10777364561105071,
                             0.10150396602136298,
                             0.10481767258337185,
                             0.1095741519955612,
                             0.1210237673045318,
                             0.12846918490636428],
                    'iram': [0.19272326081875912,
                             0.19797627035260562,
                             0.23811086426501285,
                             0.32718000832700495,
                             0.4207817877904239,
                             0.4996936045413538,
                             0.5992687604609368,
                             0.5825016998817808,
                             0.5548491245731807,
                             0.5393339913373081,
                             0.5775627522248148,
                             0.6325616481035863,
                             0.5840975656934306,
                             0.5611404170805093,
                             0.5463454640826956,
                             0.5989182197313303],
                    'jcmt': [0.03991452125297088,
                             0.049838901888596444,
                             0.07344950113691198,
                             0.1425721280589823,
                             0.2171914535883205,
                             0.26427282975449984,
                             0.2319080696215085,
                             0.15798995124302645,
                             0.1558929643497062,
                             0.20882800433000082,
                             0.25866826159112183,
                             0.2526649334224577,
                             0.24514100246196877,
                             0.16017805953145592,
                             0.22416298545007482,
                             0.19109440281935955],
                    'lmt': [0.2361563997287686,
                            0.22470543834987997,
                            0.2805148315780307,
                            0.29022007687105683,
                            0.3112219381033648,
                            0.39748312416045456,
                            0.4080680650612349,
                            0.31985235165827913,
                            0.28088139913212967,
                            0.22736396973859674,
                            0.23519236708870447,
                            0.21937043782873608,
                            0.18849964915661552,
                            0.22619118743074731,
                            0.20846222332358263,
                            0.14924964977795657],
                    'sma': [0.04012731901581167,
                            0.05022943229739918,
                            0.0739756323202303,
                            0.1430154219088304,
                            0.217676387352142,
                            0.26428862113363966,
                            0.23191317925540825,
                            0.15861162062420872,
                            0.15648050087389284,
                            0.20905352188333456,
                            0.2592181840324588,
                            0.2529404097211136,
                            0.24577577068682677,
                            0.16102460357693651,
                            0.22500256405084598,
                            0.19252827868968622],
                    'smt': [0.10667719751259586,
                            0.1748834168298549,
                            0.1512322940485475,
                            0.15203153266240144,
                            0.1785035875661887,
                            0.22689052813634944,
                            0.27415960537773426,
                            0.3320660662526106,
                            0.2660369939063821,
                            0.26163084556448063,
                            0.23940248143233744,
                            0.23536950829113204,
                            0.326987259957943,
                            0.27715235539805466,
                            0.23884673568693246,
                            0.21684953761298706],
                    'spt': [0.005707120643860627,
                            0.007666823166172434,
                            0.009747599925835005,
                            0.013412710667301988,
                            0.014952183324422384,
                            0.018293974017948696,
                            0.019830664905036408,
                            0.021346058741320874,
                            0.026040146350006853,
                            0.02741879781786002,
                            0.025891194457134163,
                            0.022205690799509636,
                            0.021335092525927503,
                            0.022277224665292607,
                            0.02375843679944221,
                            0.023605450091265703]}

    print("read_data")
    return databook, std_dict

