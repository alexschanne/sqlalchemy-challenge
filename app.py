#Importing Libraries and Dependencies
import numpy as np 
import datetime as dt 
import sqlalchemy 
from sqlalchemy.ext.automap import automap
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database Setup
engine = create_engine('sqlite://hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup 
app = Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes: <br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0.tobs<br/>"
        f"Temperature Data from start date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature Data from end date (yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    queryresult = session.query(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    queryresult = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()

    stations = []
    for station, name, lat, lng, elv in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lng"] = lng
        station_dict["Elv"] = elv
        stations.append(station_dict)

    return jsonify(stations)

@app.route("api/v1.0/tobs")


@app.route("/api/v1.0/<start>")
def get_t_start(start):
    session = Session(engine)
    queryresult = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()

    tobsall = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict['Min'] = min
        tobs_dict['Avg'] = avg
        tobs_dict['Max'] = max
        tobsall. append(tobs_dict)

    return jsonify(tobsall)

@app.route('/api/v1.0/<start>/<stop>')
def get_t_start_stop(start,stop):
    session = Session(engine)
    queryresult = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= stop).all()
    session.close()

    tobsall = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict['Min'] = min
        tobs_dict['Avg'] = avg
        tobs_dict['Max'] = max
        tobsall. append(tobs_dict)

    return jsonify(tobsall)


    
