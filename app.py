'''Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
Use FLASK to create your routes'''
# Import dependencies:
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
from collections import defaultdict

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask Setup:
app = Flask(__name__)
#Routes:
# /
    #Home page
    #List all routes that are available
@app.route("/")
def home_page():
    return(
        f"<div align='center'><h1>Welcome to my Hawaii Climate App</h1><br/></div>"
        f"<hr><br/>"
        f"<h2>Available routes:</h2><br/>"
        f"<ul>"
        f"<li><h4>A dictionary of the last 12 months of precipitation data:</h4></li>"
        f"/api/v1.0/precipitation<br/>"
        f"<li><h4>A list of all available stations:</h4></li>"
        f"/api/v1.0/stations<br/>"
        f"<li><h4>A list of  Temperature Observations (tobs) for the previous year:</h4></li>"
        f"/api/v1.0/tobs<br/>"
        f"<li><h4>A list of the minimum temperature, the average temperature, and the max temperature for all dates greater or equal to YYYY-mm-dd (example year: 2015-03-01):</h4></li>"
        f"/api/v1.0/2015-03-01<br/>"
        f"<li><h4>A list of the minimum temperature, the average temperature, and the max temperature for dates between the start and end date inclusive, formatted YYYY-mm-dd (example range: 2015-03-01 to 2016-09-06):</h4></li>"
        f"/api/v1.0/2015-03-01/2016-09-06"
        f"</ul>"
    )

#/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    # Perform a query to retrieve the data and precipitation scores

    msmt_test = session.query(Measurement).\
            order_by(Measurement.date.desc())\
            .first()
    last_test = pd.to_datetime(msmt_test.date)
    first_test = last_test - timedelta(days=365)
    first_date = dt.date(first_test.year, first_test.month, first_test.day)
    last_date = dt.date(last_test.year, last_test.month, last_test.day)

    msmt_year = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= first_date).\
        order_by(Measurement.date.asc()).\
        all()
    session.close()

    precip_data = []
    for date, prcp in msmt_year:
        precip_dict = {date:prcp}
        precip_data.append(precip_dict)
    d = defaultdict(list)
    for date,prcp in msmt_year:
        d[date].append(prcp)
    precip_dict_defaultdict = dict(d)

    # Return the JSON representation of your dictionary.
    return jsonify(precip_dict_defaultdict) #****** has null values ******

# /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Return a JSON list of stations from the dataset.
    station_count = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()#.distinct(Station.station).count()#group_by(Station.station).all()
    station_list = list(np.ravel(station_count))
    session.close()
    return(jsonify(station_list))


# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    # query for the dates and temperature observations from a year from the last data point.
    session = Session(engine)
    top_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).\
                first().station
    msmt_test = session.query(Measurement).\
            order_by(Measurement.date.desc()).\
            first()
    last_test = pd.to_datetime(msmt_test.date)
    first_test = last_test - timedelta(days=365)
    first_date = dt.date(first_test.year, first_test.month, first_test.day)

    tobs_response = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= first_date).\
        filter(Measurement.station == top_station).\
        order_by(Measurement.date.asc()).\
        all()
    tobs_list = list(np.ravel(tobs_response))
    
    session.close()
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(tobs_list)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
#   When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start_tobs(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    msmt_test = session.query(Measurement).\
            order_by(Measurement.date.desc())\
            .first()
    last_test = pd.to_datetime(msmt_test.date)
    time_btw = last_test - pd.to_datetime(start)

    test_range = pd.Series(pd.date_range(start,periods=time_btw.days+1,freq='D'))
    date_list = []
    for trip in test_range:
        date_list.append(trip.strftime('%Y-%m-%d'))
    def daily_normals(start_date):
        '''Daily Normals. 
        Args:
            date (str): A date string in the format '%Y-%m-%d'
            
        Returns:
            A list of tuples containing the daily normals, tmin, tavg, and tmax
        
        '''
    
        sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        norms = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) == start_date).all()
        return(norms)

    normals= []
    for date in date_list:
        normals.append(daily_normals(date))
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    session.close()
    return jsonify(normals)
    

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    time_btw = pd.to_datetime(end) - pd.to_datetime(start)

    test_range = pd.Series(pd.date_range(start,periods=time_btw.days+1,freq='D'))
    date_list = []
    for trip in test_range:
        date_list.append(trip.strftime('%Y-%m-%d'))
    def daily_normals(start_date):
        '''Daily Normals. 
        Args:
            date (str): A date string in the format '%Y-%m-%d'
            
        Returns:
            A list of tuples containing the daily normals, tmin, tavg, and tmax
        
        '''
    
        sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        norms = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) == start_date).all()
        return(norms)

    normals= []
    for date in date_list:
        normals.append(daily_normals(date))
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    session.close()
    return jsonify(normals)



if __name__ == '__main__':
    app.run(debug=True)
