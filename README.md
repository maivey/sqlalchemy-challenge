# sqlalchemy-challenge
You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area

- - -
## Prerequisites
This script requires imports of the following:
Graphing libraries:
```code
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
```
Import numpy and pandas:
```code
import numpy as np
import pandas as pd
```
Import libraries to handle dates and statistics:
```code
import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from scipy import stats
```
Import sqlalchemy dependencies:
```code
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
```

## Step 1 - Climate Analysis and Exploration

This script uses Python and SQLAlchemy to do basic climate analysis and data exploration of the provided climate database. All of the following analysis are completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Choose a start date and end date for your trip. Made sure that my vacation range is approximately 3-15 days total.

* Use SQLAlchemy `create_engine` to connect to the sqlite database.

* Use SQLAlchemy `automap_base()` to reflect my tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis

* Designs a query to retrieve the last 12 months of precipitation data.

* Selects only the `date` and `prcp` values.

* Loads the query results into a Pandas DataFrame and sets the index to the date column.

* Sorts the DataFrame values by `date`.

* Plots the results using the DataFrame `plot` method.

* Uses Pandas to print the summary statistics for the precipitation data.

### Station Analysis

* Designs a query to calculate the total number of stations.

* Designs a query to find the most active stations.

  * Lists the stations and observation counts in descending order.

  * Determines which station has the highest number of observations


* Designs a query to retrieve the last 12 months of temperature observation data (tobs).

  * Filters by the station with the highest number of observations.

  * Plots the results as a histogram with `bins=12`.

- - -

## Step 2 - Climate App

After completing the initial analysis, a Flask API is designed based on the queries that have just been developed.

* Use FLASK to create the routes.

### Routes

* `/`

  * Home page.

  * Lists all routes that are available.

* `/api/v1.0/precipitation`

  * Converts the query results to a Dictionary using `date` as the key and `prcp` as the value.

  * Returns the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * queries for the dates and temperature observations from a year from the last data point.
  * Returns a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculates `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculates the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

- - -

## Other Analyses


### Temperature Analysis I

* Hawaii is reputed to enjoy mild weather all year. Included in the script, determines if there a meaningful difference between the temperature in, for example, June and December?


* Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

* Paired t-test:

Hypothesis Test:
```text
H0 : uj = ud (The means are the same)
Ha : uj != ud (The means are different)
```
Testing at ```alpha = 0.05```

I used paired t-test since the two variables, average tobs in June and average tobs in December, are taken from the same stations, but at different times. Since the average tobs in June can be paired with the average tobs in December, we use a paired t-test. Additionally, there are no obvious outliers in each sample, as shown in the Box Plot below.

Results:

The p-value is ```0.0032683642779833687```

Testing at alpha=0.05, since p=0.0032683642779833687 < alpha=0.05, the findings are statistically significant. We can reject the null hypothesis in support of the alterative with 95% confidence.

### Temperature Analysis II

* Uses the `calc_temps` function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if my trip start date was "2018-01-01").

* Plots the min, avg, and max temperature from my previous query as a bar chart.

  * Uses the average temperature as the bar height.

  * Uses the peak-to-peak (tmax-tmin) value as the y error bar (yerr).


### Daily Rainfall Average

* Calculates the rainfall per weather station using the previous year's matching dates.

* Calculates the daily normals. Normals are the averages for the min, avg, and max temperatures.

* A function called `daily_normals` calculates the daily normals for a specific date. This date string will be in the format `%m-%d`.

* Creates a list of dates for my trip in the format `%m-%d`. Uses the `daily_normals` function to calculate the normals for each date string and append the results to a list.

* Loads the list of daily normals into a Pandas DataFrame and set the index equal to the date.

* Uses Pandas to plot an area plot (`stacked=False`) for the daily normals.
