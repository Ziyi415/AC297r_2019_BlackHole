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

Our models and software are packaged in `src/` folder which will be explained in Software Organization section. `notebooks/` and `submissions/` include our whole development process, presentation slides and other related files throughout the course. Introduction to this project, including background, problem statement, model designs and evaluation can be found in this article here: <a href="https://medium.com/@ziyi_zhou/optimal-real-time-scheduling-for-black-hole-imaging-e129b33db160">Optimal Real-time Scheduling for Black Hole Imaging</a>.

# How to install

To install our software



# Software Organization

The `src/` folder stores all our models and software. 

In `model/`, `make_suggestions.py` includes all four methods described <a href="https://medium.com/@ziyi_zhou/optimal-real-time-scheduling-for-black-hole-imaging-e129b33db160">here</a>. Most of the calculation and data cleaning process is written in its dependencies, `processing_data.py` and `read_data.py`. 

`settings.py` sets the basic settings and parameters for running our model which include forecast data path, telescope names, window information and scheduling information. With `write_file.py`, these settings are also connected to our software where you can accessed and modified them. Although it is preferred to use our software to access the settings, you can still update the file directly and run our models via python scripting.

`forecast_data/` folder includes all the weather forecast data we pulled from the Global Forecast System (GFS) from 10/25/2019 to 11/30/2019, whereas `data/` folder [also stores the parameters???] Currently, the data path defined in `settings.py` is the path to `forecast_data/`.

[`windows/`, `images/`....]

`evaluation_results/` has the model evaluation results from backtesting. The paths and scores are produced by all our models with different penalty levels on the training data, and are used for model comparison. Still, details can be found in our <a href="https://medium.com/@ziyi_zhou/optimal-real-time-scheduling-for-black-hole-imaging-e129b33db160">blog post</a>.

`test.py` includes an example to run our model and make a path suggestion in python.


# How to use our software

Please refer to the video demo of our software. <a href="https://www.youtube.com/watch?v=UKHaZE5Ws6c">EHT software demo</a>


# How to use our package



--------


<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
