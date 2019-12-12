Optimal Real-time Schedualing for Black Hole Imaging
==============================

AC297r Capstone

This is our project repository for Harvard IACS Capstone course (Fall 2019). We are Shu Xu, Yiming Xu and Ziyi(Queena) Zhou, Master's students in Data Science at Harvard University.

Project Organization
------------

    ├── Makefile
    ├── README.md
    ├── notebooks/
    ├── requirements.txt
    ├── setup.py
    ├── src/
    │   ├── __init__.py
    │   ├── model/                      python scripts for our models
    │   ├── forecast_data/              data pulled from GFS for each site
    │   ├── data/                       input parameters
    │   ├── windows/                    source code for our software
    │   ├── images/                     
    │   ├── app.py                      run our software
    │   ├── evaluation_results/         model evaluation results
    │   ├── evaluate.py                 model evaluation script
    │   └── test.py                     run our model and make a suggestion
    ├── submissions/
    │   ├── final-presentation
    │   ├── lighting-talk-1
    │   ├── lighting-talk-2
    │   ├── midterm
    │   ├── milestone-1
    │   ├── milestone-2
    │   ├── milestone-3   
    │   └── partners-reports
    └── test_project.py

Our models and software are packaged in `src/` folder and is explained in Software Organization section. `notebooks/` and `submissions/` include our whole development process, presentation slides and other related files throughout the course. Introduction to this project, including background, problem statement, model designs and evaluation can be found in this blog post: <a href="https://medium.com/@ziyi_zhou/optimal-real-time-scheduling-for-black-hole-imaging-e129b33db160">Optimal Real-time Scheduling for Black Hole Imaging</a>.

# How to install

To install our software



# Software Organization

The `src/` folder stores all our models and software. 

In `model/`, `make_suggestions.py` includes all four methods described <a href="https://medium.com/@ziyi_zhou/optimal-real-time-scheduling-for-black-hole-imaging-e129b33db160">here</a>. Most of the calculation and data cleaning process is written in its dependencies, `processing_data.py` and `read_data.py`. 

`settings.py` sets the basic settings and parameters for running our model which include forecast data path, telescope names, window information and scheduling information. With `write_file.py`, these settings are also connected to our software where you can accessed and modified them. Although it is preferred to use our software to access the settings, you can still update the file directly and run our models via python scripting.

`forecast_data/` folder includes all the weather forecast data we pulled from the Global Forecast System (GFS) from 10/25/2019 to 11/30/2019, whereas `data/` folder [also stores the parameters???] Currently, the data path defined in `settings.py` is the path to `forecast_data/`.

[`windows/`, `images/`....]

`evaluation_results/` has the model evaluation results from backtesting, which is the output of `evaluate.py`. The paths and scores are produced by all our models with different penalty levels on the training data, and are used for model comparison. Still, details can be found in our <a href="https://medium.com/@ziyi_zhou/optimal-real-time-scheduling-for-black-hole-imaging-e129b33db160">blog post</a>.

`test.py` includes an example to run our model and make a path suggestion in python.


# How to use our software

Please refer to the video demo of our software. <a href="https://www.youtube.com/watch?v=UKHaZE5Ws6c">EHT software demo</a>


# How to use our package

Once you have downloaded our package (`model/`) and place it in the same folder as your scripts, you can import the moduls:

```python
from model import make_suggestions, processing_data, read_data
from model import settings
import pandas as pd
```
Make sure you have modified `data_path` in `settings.py` to be the folder where you store the weather forecast pulled from GFS, and under `data_path`, there is a folder for each telescope site and the folder name matches `telescopes` in `settings.py`. Suppose you'd like to make a decision in the window `(settings.start_date, settings.end_date)`, you probably want to include the weather forecast data for the previous day of `settings.start_date`, as three of our models require historical data.

Then you can load the data by typing in:

```python
databook, std_dict = read_data.run_read_data(settings.start_date, settings.end_date)
```
where `databook` is a python dictionary of all the tau225 data across sites and days and `std_dict` is the weather forecast variance we calculated.

**To make a suggested path**

```python
should_trigger, selected_future_days, confidence_level, each_day_score, second_optimal, second_optimal_prob = function(
            start_date, end_date, databook, std_dict, num_days_left, punish_level)
```

**Input:** 

`function` should be is one of our four methods,`make_suggestions.decision_making_single_punishment`, `make_suggestions.decision_making_further_std_punishment`, `make_suggestions.decision_making_time_std_punishment` and `make_suggestions.decision_making_sampling`, which correspond to method 1 to method 4 (described in the <a href="https://medium.com/@ziyi_zhou/optimal-real-time-scheduling-for-black-hole-imaging-e129b33db160">blog post</a>) accordingly. 

`start_date`, `end_date`, `num_days_left` could be specified here in spite of what's in `settings.py`, but we recommend using `settings.start_date`, `settings.end_date` and `settings.days_left` consistently as in our `test.py` example.

`punish_level` is the hyperparameter for the first three models. Its default value is already set to the best penalty level validated by model evaluation.

**Output:**

`should_trigger` indicates whether the model suggests to trigger the `start_date`, and `selected_future_days` is the suggested path. `each_day_score` is an array of scores calculated by the model for each day, and the suggested path include the days with the best scores. Only the last model will return `confidence_level`, `second_optimal`, `second_optimal_prob` instead of `None`.

There is a runnable example in `test.py`. For detailed evaluation process, see `evaluate.py`.


--------


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
