from model import make_suggestions
from model import settings, read_data, processing_data
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def make_one_path(start_date, end_date, num_days_left, function, punish_level = 0, distance = True, use_as_evaluate=False):

    if num_days_left <= 0:
        return None, None, None, None
    
    should_trigger, selected_future_days, confidence_level, each_day_score, _, _= function(start_date, end_date, num_days_left, punish_level, distance, use_as_evaluate=use_as_evaluate)

    return should_trigger, selected_future_days, confidence_level, each_day_score

def simulate(start_date, end_date, num_days_left, function, punish_level = 0, distance = True):
    start_dt = datetime.strptime(start_date,"%Y-%m-%d")
    end_dt = datetime.strptime(end_date,"%Y-%m-%d")
    date_list = np.arange(start_dt, end_dt+timedelta(days=1),timedelta(days=1)).astype(datetime)
    date_list = [t.strftime("%Y-%m-%d") for t in date_list]

    path = []
    for i,start_date in enumerate(date_list):
        should_trigger, _, _, _ = make_one_path(start_date, end_date, num_days_left, function, punish_level=punish_level, distance = distance)
        if should_trigger:
            path.append(start_date)
            num_days_left -= 1
            
    return path

def compute_score(start_date, end_date, path, each_day_reward):
    '''compute a score given each day reward and path
    path: a list of selected dates, e.g. ['2019-11-07', '2019-11-06']
    each_day_reward: an array that matchs the length from start_date to end_date
    '''
    # get consecutive date list whose length = length of each_day_reward
    start_date = datetime.strptime(start_date,"%Y-%m-%d")
    end_date = datetime.strptime(end_date,"%Y-%m-%d")
    date_list = np.arange(start_date, end_date+timedelta(days=1),timedelta(days=1)).astype(datetime)
    date_list = [t.strftime("%Y-%m-%d") for t in date_list]
    # calculate score for this path
    score = 0
    for day, reward in zip(date_list,np.array(each_day_reward)):
        if day in path:
            score += reward
    score = score/len(path)
    # compare with random path based on predictions if evaluate a future path
    _ = np.mean(each_day_reward)
    return score

############### organizing validation dataset ################
# available training data
available_data_start = "2019-10-26" # same as in settings.py
available_data_end = "2019-11-30"

# setting: a 10 choose 5 problem
window_length = 10 
days_left = 5

# make a list of start+end pairs
start_end_pair_list = [] 
start = datetime.strptime(available_data_start,"%Y-%m-%d")
end = start
while end < datetime.strptime(available_data_end,"%Y-%m-%d"):
    end = start + timedelta(days=window_length-1)
    start_end_pair_list.append((start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d")))
    start = start + timedelta(days=1)

### get best path and best path score for each start-end pair
path_results = []
score_results = []
for (start_date, end_date) in start_end_pair_list:

    # The best path when we look back, and get true reward at the same time by setting use_as_evaluate=True and default punish level=0
    _, best_path, _, each_day_true_reward = make_suggestions.decision_making_single_punishment(start_date, end_date, days_left, use_as_evaluate=True)

    # when look back, scores are all computed from each_day_true_reward which is not discounted
    # best path's score when look back
    best_path_score = compute_score(start_date, end_date, best_path, each_day_true_reward)

    # random path expectation score when look back
    random_expect_score = np.mean(each_day_true_reward)
    
    # record results in the dataframe
    path_results.append({'range':(start_date, end_date), 'true_reward':each_day_true_reward,'best_path': best_path})
    score_results.append({'range':(start_date, end_date), \
                          'best_score':best_path_score,'random_score':random_expect_score})
    
path_results = pd.DataFrame.from_dict(path_results, orient='columns')
score_results = pd.DataFrame.from_dict(score_results, orient='columns')

# checkpoint - save data
path_results.to_csv("evaluation_results/path_results.csv")
score_results.to_csv("evaluation_results/score_results.csv")

####################################################################################
#### decision_making_single_punishment (model1) ####################################
####################################################################################

punish_level_list = [0,0.04,0.06,0.08,0.1,0.2]

### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date, days_left, \
                make_suggestions.decision_making_single_punishment, pl, settings.baseline_lengths)

        # The best path when we look back, and get true reward at the same time by setting use_as_evaluate=True and default punish level=0
#         _, best_path, _, each_day_true_reward = make_suggestions.decision_making_single_punishment(start_date, end_date, days_left, use_as_evaluate=True)
        each_day_true_reward = path_results['true_reward'][path_results['range']==(start_date, end_date)].values[0]
#         # when look back, scores are all computed from each_day_true_reward which is not discounted
#         # best path's score when look back
#         best_path_score = compute_score(start_date, end_date, best_path, each_day_true_reward)

#         # random path expectation score when look back
#         random_expect_score = np.mean(each_day_true_reward)
        
        # our path's score when look back
        our_path_score = compute_score(start_date, end_date, our_path, each_day_true_reward)
        
        print("Punish level =", pl)
        print("Date range:", start_date, end_date)
        path_col.append(our_path)
        score_col.append(our_path_score)
    path_results['model1_punish_'+str(pl)] = path_col
    score_results['model1_punish_'+str(pl)] = score_col
    
# checkpoint - save results
path_results.to_csv("evaluation_results/path_results.csv")
score_results.to_csv("evaluation_results/score_results.csv")

####################################################################################
#### decision_making_further_std_punishment (model2) ###############################
####################################################################################

punish_level_list = [0,1,5,10]

### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date, days_left, \
                make_suggestions.decision_making_further_std_punishment, pl, settings.baseline_lengths)

        # The best path when we look back, and get true reward at the same time by setting use_as_evaluate=True and default punish level=0
#         _, best_path, _, each_day_true_reward = make_suggestions.decision_making_single_punishment(start_date, end_date, days_left, use_as_evaluate=True)
        each_day_true_reward = path_results['true_reward'][path_results['range']==(start_date, end_date)].values[0]


#         # when look back, scores are all computed from each_day_true_reward which is not discounted
#         # best path's score when look back
#         best_path_score = compute_score(start_date, end_date, best_path, each_day_true_reward)

#         # random path expectation score when look back
#         random_expect_score = np.mean(each_day_true_reward)
        
        # our path's score when look back
        our_path_score = compute_score(start_date, end_date, our_path, each_day_true_reward)
        
        print("Punish level =", pl)
        print("Date range:", start_date, end_date)
        path_col.append(our_path)
        score_col.append(our_path_score)
    path_results['model2_punish_'+str(pl)] = path_col
    score_results['model2_punish_'+str(pl)] = score_col
    
# checkpoint - save results
path_results.to_csv("evaluation_results/path_results.csv")
score_results.to_csv("evaluation_results/score_results.csv")

####################################################################################
#### decision_making_time_std_punishment (model2) ##################################
####################################################################################

punish_level_list = [0,1,5,10]

### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date, days_left, \
                make_suggestions.decision_making_time_std_punishment, pl, settings.baseline_lengths)

        # The best path when we look back, and get true reward at the same time by setting use_as_evaluate=True and default punish level=0
#         _, best_path, _, each_day_true_reward = make_suggestions.decision_making_single_punishment(start_date, end_date, days_left, use_as_evaluate=True)
        each_day_true_reward = path_results['true_reward'][path_results['range']==(start_date, end_date)].values[0]


#         # when look back, scores are all computed from each_day_true_reward which is not discounted
#         # best path's score when look back
#         best_path_score = compute_score(start_date, end_date, best_path, each_day_true_reward)

#         # random path expectation score when look back
#         random_expect_score = np.mean(each_day_true_reward)
        
        # our path's score when look back
        our_path_score = compute_score(start_date, end_date, our_path, each_day_true_reward)
        
        print("Punish level =", pl)
        print("Date range:", start_date, end_date)
        path_col.append(our_path)
        score_col.append(our_path_score)
    path_results['model3_punish_'+str(pl)] = path_col
    score_results['model3_punish_'+str(pl)] = score_col
    
# checkpoint - save results
path_results.to_csv("evaluation_results/path_results.csv")
score_results.to_csv("evaluation_results/score_results.csv")

####################################################################################
#### decision_making_sampling (model2) #############################################
####################################################################################

punish_level_list = [0]

### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date, days_left, \
                make_suggestions.decision_making_time_std_punishment, pl, settings.baseline_lengths)

        # The best path when we look back, and get true reward at the same time by setting use_as_evaluate=True and default punish level=0
#         _, best_path, _, each_day_true_reward = make_suggestions.decision_making_single_punishment(start_date, end_date, days_left, use_as_evaluate=True)
        each_day_true_reward = path_results['true_reward'][path_results['range']==(start_date, end_date)].values[0]


#         # when look back, scores are all computed from each_day_true_reward which is not discounted
#         # best path's score when look back
#         best_path_score = compute_score(start_date, end_date, best_path, each_day_true_reward)

#         # random path expectation score when look back
#         random_expect_score = np.mean(each_day_true_reward)
        
        # our path's score when look back
        our_path_score = compute_score(start_date, end_date, our_path, each_day_true_reward)
        
        print("Punish level =", pl)
        print("Date range:", start_date, end_date)
        path_col.append(our_path)
        score_col.append(our_path_score)
    path_results['model4_punish_'+str(pl)] = path_col
    score_results['model4_punish_'+str(pl)] = score_col

# checkpoint - save results
path_results.to_csv("evaluation_results/path_results.csv")
score_results.to_csv("evaluation_results/score_results.csv")

####################################################################################
#### result analysis (all models) ##################################################
####################################################################################


# reload result dataset
path_results = pd.read_csv("evaluation_results/path_results.csv", index_col = 0)
score_results = pd.read_csv("evaluation_results/score_results.csv", index_col = 0)

convert_reward = lambda x: [float(a.strip("\n")) for a in x.strip("[] ").split(" ") if a != ""]
path_results['true_reward'] = path_results['true_reward'].apply(convert_reward)
path_results['range'] = path_results['range'].apply(lambda x: eval(x))
score_results['range'] = score_results['range'].apply(lambda x: eval(x))

# Compare score across different models: 
# MSE = mean((model_score - best_score)^2). 
# The mean is taken across different (start_date, end_date) pairs.

mse = {}
for col in score_results.columns[3:]:
    mse[col] = ((score_results[col] - score_results['best_score'])**2).mean()

mse = pd.Series(mse)
mse.sort_values()