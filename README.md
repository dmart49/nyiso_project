# NYISO Power Analysis

## Introduction
---------------

The goal of this project was to try and forecast energy usage in New York State using data from New York's power grid collected from the New York Idependent Service Operator (NYISO). <a href= 'https://www.nyiso.com/load-data'>Load data</a> was collected by NYISO on a 5 minute basis and available on their <a href ='https://www.nyiso.com/'>website</a> dating back to 2001. This data was taken and downsampled to an hourly basis and then used in Prophet and XGboost models to predict the load required for the next 24 hours. 


## Overview
---------------

Notebook overview: <br>
<a href="https://github.com/dmart49/nyiso_project/blob/master/combinedata.ipynb">combinedata</a> - Combines all the individual .csv files, downsamples and creates a single csv file with all data <br>
<a href="https://github.com/dmart49/nyiso_project/blob/master/prophet.ipynb">prophet</a> - time series model with Prophet <br>
<a href="https://github.com/dmart49/nyiso_project/blob/master/xgboost_final.ipynb">xgboost_final</a> - a time series model with xgboost and a clean notebook with the final model used with a plotly rangeslider visualization <br>
<a href="https://github.com/dmart49/nyiso_project/blob/master/functions.py">functions</a> - all the relevant functions used in all notebooks <br>
