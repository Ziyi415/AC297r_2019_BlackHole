#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# # This notebook was developed in src/ folder
# # run this if this notebook is in notebooks/ foler
# import sys
# sys.path.append('../src/')


# In[ ]:


from model import make_suggestions
from model import settings, read_data, processing_data
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


# In[16]:


def make_one_path(start_date, end_date,databook, std_dict, num_days_left, function, punish_level = 0, distance = True, use_as_evaluate=False):
    '''Given a window and forecast data on day 1, return the suggested path. 
    This is NOT a complete simulation because on the next day, weather forecast get updated and path should be updated.'''
    if num_days_left <= 0:
        return None, None, None, None
    
    should_trigger, selected_future_days, confidence_level, each_day_score, _,_= function(start_date, end_date,databook, std_dict, num_days_left, punish_level, distance, use_as_evaluate=use_as_evaluate)

    return should_trigger, selected_future_days, confidence_level, each_day_score

def simulate(start_date, end_date,databook, std_dict, num_days_left, function, punish_level = 0, distance = True):
    '''simulate a complete decision making process in a 10 day window'''
    start_dt = datetime.strptime(start_date,"%Y-%m-%d")
    end_dt = datetime.strptime(end_date,"%Y-%m-%d")
    date_list = np.arange(start_dt, end_dt+timedelta(days=1),timedelta(days=1)).astype(datetime)
    date_list = [t.strftime("%Y-%m-%d") for t in date_list]

    path = []
    for i,start_date in enumerate(date_list):
        should_trigger, _, _, _ = make_one_path(start_date, end_date,databook, std_dict, num_days_left, function, punish_level=punish_level, distance = distance)
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


# ## Training data and ground-truth best path
# Read in training data and get all consecutive 10-day window.

# In[ ]:


# available training data
available_data_start = "2019-10-25" 
first_window_start = "2019-10-26" # our model requires at least 1 day historical data to compute the variance of weather forecast
available_data_end = "2019-11-30"

# read in data
databook, std_dict = read_data.run_read_data(available_data_start, available_data_end)

# setting: a 10 choose 5 problem
window_length = 10 
days_left = 5

# make a list of start+end pairs
start_end_pair_list = [] 
start = datetime.strptime(first_window_start,"%Y-%m-%d") 
end = start
while end < datetime.strptime(available_data_end,"%Y-%m-%d"):
    end = start + timedelta(days=window_length-1)
    start_end_pair_list.append((start.strftime("%Y-%m-%d"),end.strftime("%Y-%m-%d")))
    start = start + timedelta(days=1)


# In[ ]:


start_end_pair_list


# Get ground-truth best path and best path score in every window

# In[ ]:


### get best path and best path score for each start-end pair
path_results = []
score_results = []
for (start_date, end_date) in start_end_pair_list:

    # The best path when we look back, and get true reward at the same time by setting use_as_evaluate=True and default punish level=0
    _, best_path, _, each_day_true_reward, _,_ = make_suggestions.decision_making_single_punishment(start_date, end_date,databook, std_dict, days_left, use_as_evaluate=True)

    # when look back, scores are all computed from each_day_true_reward which is not discounted
    # best path's score when look back
    best_path_score = compute_score(start_date, end_date, best_path, each_day_true_reward)

    # random path expectation score when look back
    random_expect_score = np.mean(each_day_true_reward)
    
    # record results in the dataframe
    path_results.append({'range':(start_date, end_date), 'true_reward':each_day_true_reward,'best_path': best_path})
    score_results.append({'range':(start_date, end_date),                           'best_score':best_path_score,'random_score':random_expect_score})
    
path_results = pd.DataFrame.from_dict(path_results, orient='columns')
score_results = pd.DataFrame.from_dict(score_results, orient='columns')


# In[ ]:


path_results.to_csv("path_results.csv")
score_results.to_csv("score_results.csv")


# ### Method 1: discount factor
# 
# find best penalty level for method 1: `make_suggestions.decision_making_single_punishment`

# In[ ]:


punish_level_list = [0,0.01, 0.02,0.03,0.04,0.05,0.06,0.08,0.1,0.2]


# In[ ]:


### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date, databook, std_dict, days_left,                 make_suggestions.decision_making_single_punishment, pl, settings.baseline_lengths)

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
    
score_results


# In[ ]:


path_results.to_csv("path_results.csv")
score_results.to_csv("score_results.csv")


# ### Method 2: forecast penalty
# 
# find best penalty level for method 2: `make_suggestions.decision_making_further_std_punishment`

# In[ ]:


punish_level_list = [0,0.2,0.4,0.6,0.8,1,2,5,10]


# In[ ]:


### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date, databook, std_dict, days_left,                 make_suggestions.decision_making_further_std_punishment, pl, settings.baseline_lengths)

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
    
score_results


# In[ ]:


path_results.to_csv("path_results.csv")
score_results.to_csv("score_results.csv")


# ### Method 3: prediction difficulty of specific time
# 
# find best penalty level for method 2: `make_suggestions.decision_making_time_std_punishment`

# In[ ]:


punish_level_list = [0,0.1,0.5,0.6,0.8,1,1.2,3,5]


# In[ ]:


### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date,databook, std_dict,  days_left,                 make_suggestions.decision_making_time_std_punishment, pl, settings.baseline_lengths)

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
    
score_results


# In[ ]:


path_results.to_csv("path_results.csv")
score_results.to_csv("score_results.csv")


# ### Method 4: sampling from normal
# 
# no penalty defined for `make_suggestions.decision_making_sampling`

# In[13]:


punish_level_list = [0]


# In[17]:


### get model selected path and score for each start-end pair and different punishment level
for pl in  punish_level_list:
    path_col = []
    score_col = []
    for (start_date, end_date) in start_end_pair_list:

        # this is the path chosen by our model
        # we should update the path every day and get the final path
        our_path = simulate(start_date, end_date, databook, std_dict, days_left,                 make_suggestions.decision_making_sampling, pl, settings.baseline_lengths)

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
    
score_results


# In[ ]:


path_results


# In[18]:


path_results.to_csv("path_results.csv")
score_results.to_csv("score_results.csv")


# ----

# ## Result Analysis

# In[41]:


# reload result dataset
path_results = pd.read_csv("evaluation_results/path_results.csv", index_col = 0)
score_results = pd.read_csv("evaluation_results/score_results.csv", index_col = 0)

# some data formatting was changed when we save csv, so we change it back
convert_reward = lambda x: [float(a.strip(",\n")) for a in x.strip("[] ").split(" ") if a != ""]
path_results['true_reward'] = path_results['true_reward'].apply(convert_reward)
path_results['range'] = path_results['range'].apply(lambda x: eval(x))
path_results['best_path'] = path_results['best_path'].apply(lambda x: [d.strip("''") for d in x.strip("[]").split(" ")])
score_results['range'] = score_results['range'].apply(lambda x: eval(x))


# See result for one window: (11/09-11/18)

# In[77]:


# path_results['best_path_numeric'] = path_results['true_reward'].apply(lambda x: np.argsort(x)[-days_left:].sum())

window_example_score = score_results.loc[14][['range','best_score','random_score','model1_punish_0',                      'model3_punish_1','model2_punish_0.6','model1_punish_0.03','model4_punish_0']]
window_example_score


# In[78]:


window_example = path_results.loc[14][['range','true_reward','best_path','best_path_numeric','model1_punish_0',                      'model3_punish_1','model2_punish_0.6','model1_punish_0.03','model4_punish_0']]
for i in enumerate(window_example):
    print(i)


# Compare different punishment level within a model: how many times a (model, punish_level) hits to the best path among all different punishment levels given the same model:

# In[42]:


eval(path_results[model1_cols].loc[0]['model1_punish_0'])


# In[74]:


model1_cols = [col for col in score_results.columns if 'model1' in col]
model1_cols.sort()

best_model1 = path_results[['range','best_path']].copy()

for col in model1_cols:
    model_paths = path_results[col].apply(eval)
    hit_best_counts = []
    for modelpath, bestpath in zip(model_paths, path_results['best_path']):
        hit_best_counts.append(len(set(modelpath)&set(bestpath)))
    best_model1[col] = hit_best_counts
    
best_model1.sum()


# In[73]:


model2_cols = [col for col in score_results.columns if 'model2' in col]
model2_cols.sort()

best_model2 = path_results[['range','best_path']].copy()

for col in model2_cols:
    model_paths = path_results[col].apply(eval)
    hit_best_counts = []
    for modelpath, bestpath in zip(model_paths, path_results['best_path']):
        hit_best_counts.append(len(set(modelpath)&set(bestpath)))
    best_model2[col] = hit_best_counts
    
best_model2.sum()


# In[72]:


model3_cols = [col for col in score_results.columns if 'model3' in col]
model3_cols.sort()

best_model3 = path_results[['range','best_path']].copy()

for col in model3_cols:
    model_paths = path_results[col].apply(eval)
    hit_best_counts = []
    for modelpath, bestpath in zip(model_paths, path_results['best_path']):
        hit_best_counts.append(len(set(modelpath)&set(bestpath)))
    best_model3[col] = hit_best_counts
    
best_model3.sum()


# Compare different models: 
# 
# MSE = mean((model_score - best_score)^2). The mean is taken across different (start_date, end_date) pairs.
# relative score = mean((model_score - random_score)/(best_score - random_score))

# In[75]:


### MSE
mse = {}
### relative score
relative = {}
for col in score_results.columns[2:]:
    mse[col] = ((score_results[col] - score_results['best_score'])**2).mean()
    relative[col] = ((score_results[col] - score_results['random_score'])/(score_results['best_score'] - score_results['random_score'])).mean()

mse = pd.Series(mse)
relative = pd.Series(relative)
mse.sort_values()


# In[76]:


relative.sort_values(ascending = False)


# In[ ]:




