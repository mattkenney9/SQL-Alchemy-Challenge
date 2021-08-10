#imports
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#set up DataBase
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)
app = Flask(__name__)


Base = automap_base()
Base.prepare(engine, reflect= True)

Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    return(
        f"Welcome to the Hawaii Precipitation API!<br/>"
        f"Avialable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<<br/>"
    )

#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_back).\
        order_by(Measurement.date).all()
    session.close()
    precip_data_list = dict(precip_data)
    return jsonify(precip_data_list)

#Stations Route
@app.route("/api/v1.0/stations")
def stations():
    station_qry = session.query(Station.station, Station.name).\
        order_by(Station.name).all()
    stations_list = list(station_qry)
    return jsonify(stations_list)


#tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
    yearset = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= yearset).all()
    tobs_list = dict(tobs_data)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def startset(start):
    yearset = dt.date(2017,8,23) - dt.timedelta(days=365)
    starter = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= yearset).all()
    session.close()
    starter_list = list(starter)
    return jsonify(starter_list)

@app.route("/api/v1.0/<start>/<end>")
def endset(start, end):
    endset = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= yearset).all()
    session.close()
    endset_list = list(endset)
    return jsonify(endset_list)


#main
if __name__ == '__main__':
    app.run(debug=True)
