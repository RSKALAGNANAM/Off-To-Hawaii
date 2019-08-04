import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import distinct
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
from datetime import datetime, timedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/begin/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data"""
    # Query precipitation data
    session = Session(engine)
    # Determine last_date in the Table; this is a String type
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    #Convert to datetime type from String
    end = datetime.strptime(last_date, '%Y-%m-%d')
    #Establish the date which is 12 months before the last date and this is in the datetime type
    twelve_months_prior = end - timedelta(days=366)
    #Now perform the query
    prcp_results=session.query(func.avg(Measurement.prcp), Measurement.date).\
        group_by(Measurement.date).filter(Measurement.date.between(twelve_months_prior, end))

    # Define a dictionary and from the row data and append to a list of prcp_data
    prcp_data=[]
    for prcp, date in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_data.append(prcp_dict)
        
    # Convert list of tuples into normal list
    all_prcp_data = list(np.ravel(prcp_data))

    return jsonify(all_prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of weather stations"""
    # Query all Stations
    session = Session(engine)
    
    # This is one way of doing it by querying the Measurement Table and getting a count
    # I have commented out the code because I used the Station Table instead

    #station_results = session.query(Measurement.station, func.count(Measurement.station)).\
    #                group_by(Measurement.station).order_by(desc(func.count(Measurement.station))).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    #station_data=[]
    #for station in station_results:
    #    station_dict = {}
    #    station_dict["Station Name"] = station
    #    station_data.append(station_dict)

    #return jsonify(station_data)

    # It is easier to do this by querying the Station Table given it has unique
    # rows for each station

    station_results = session.query(Station.station)

    # Create a dictionary from the row data and append to a list of station_data
    station_data=[]
    for station in station_results:
        station_dict = {}
        station_dict["Station Name"] = station
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return Temperature data for the most active Station"""
    # Query Temperature data
    session = Session(engine)
    # Determine last_date in the Table; this is a String type
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    #Convert to datetime type from String
    last = datetime.strptime(last_date, '%Y-%m-%d')
    #Establish the date which is 12 months before the last date and this is in the datetime type
    twelve_months = last - timedelta(days=366)
    #Now perform the query
    temp_results=session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == "USC00519281").\
           filter(Measurement.date.between(twelve_months, last))

    # Define a dictionary and from the row data and append to a list of prcp_data
    temp_data=[]
    for tobs, date in temp_results:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
        temp_data.append(temp_dict)
        
    # Convert list of tuples into normal list
    all_temp_data = list(np.ravel(temp_data))

    return jsonify(all_temp_data)

@app.route("/api/v1.0/<start>")
# In the URL, the date should be entered, as follows:
#  http://127.0.0.1:5000/api/v1.0/2017-04-16

def start(start):
    session = Session(engine)
    
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start).all()

    return jsonify(result)


@app.route("/api/v1.0/<begin>/<end>", endpoint='page2')
# In the URL, the dates should be entered, as follows:
#  http://127.0.0.1:5000/api/v1.0/2017-04-16/2017-05-01

def start(begin,end):
    session = Session(engine)
    if begin > end:
        return jsonify({"Error": "The begin date cannot be past the end date. Please verify the dates and retry."}), 404
    else:
        result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= begin).filter(Measurement.date <= end).all()
        return jsonify(result)
    

if __name__ == '__main__':
    app.run(debug=True)
