# Import all needed libraries
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#######################################################
# Database setup
# create engine to hawaii.sqlite
database_path = "Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#######################################################

# Create an app, being sure to pass __name__
app = Flask(__name__)

#######################################################
# Home page
# List all routes that are available
@app.route("/")
def home():
    """List of all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#######################################################
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitaion():
    
    # Create our session from Python to the database
    session = Session(engine)

    # Query all dates and prcp measurements
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    #Create a dictionary from the row data and append to a list 
    all_prcp = []
    for date, prcp, in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)
#######################################################
# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():

    # Create our session from Python to the database
    session = Session(engine)

    # Query all stations
    results = session.query(Station.name, Station.id, Station.station).all()
    session.close()

    return jsonify(results)
#######################################################
# Query the dates and temperature observations of the most active station for the last year of data
# Return a JSON list of temperature observations (TOBS) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session from Python to the database
    session = Session(engine)

    # Query dates and tobs measurements of most active station for last year
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').\
        filter(Measurement.station == 'USC00519281').all()
    session.close()

    return jsonify(results)
#######################################################
# Return a JSON list of the minimum temperature, the average temperature, 
#   and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, 
#   and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def min(start):

    # Create our session from Python to the database
    session = Session(engine)

    # Query dates to find first date
    first = session.query(Measurement).order_by(Measurement.date.asc()).first()
    #first = '2010-01-01'
    session.close()

    # Query dates and tobs measurements greater than start date
    #   to find the minimum tobs
    lowest = session.query(Measurement.tobs, Measurement.date, func.min(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').all()
    session.close()

    lowest = [{"Date": lowest[0][1], "Minimum": lowest[0][0]}]

    # Query dates and tobs measurements greater than start date
    #   to find the average tobs
    avg = session.query(Measurement.tobs, Measurement.date, func.avg(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').all()
    session.close()

    avg = [{"Date": avg[0][1], "Average": avg[0][2]}]
    
    # Query dates and tobs measurements greater than start date
    #   to find the maximum tobs
    max = session.query(Measurement.tobs, Measurement.date, func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').all()
    session.close()

    max = [{"Date": max[0][1], "Maximum": max[0][0]}]
    
    return jsonify(lowest,avg,max)
#######################################################
# Return a JSON list of the minimum temperature, the average temperature, 
#   and the max temperature for a given start or start-end range.
#  When given the start and the end date, calculate the TMIN, TAVG, 
#   and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def minmax(start,end):

    # Create our session from Python to the database
    session = Session(engine)

    # Query dates to find last date
    last = session.query(Measurement).order_by(Measurement.date.desc()).first()
    session.close()
    #last = '2017-08-23'

    # Query dates and tobs measurements greater than start date and less than end date
    #   to find the minimum tobs
    min2 = session.query(Measurement.tobs, Measurement.date, func.min(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= '2017-08-23').all()
    session.close()

    min2 = [{"Date": min2[0][1], "Minimum": min2[0][0]}]

    # Query dates and tobs measurements greater than start date and less than end date
    #   to find the average tobs
    avg2 = session.query(Measurement.tobs, Measurement.date, func.avg(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= '2017-08-23').all()
    session.close()

    avg2 = [{"Date": avg2[0][1], "Minimum": avg2[0][2]}]

    # Query dates and tobs measurements greater than start date and less than end date
    #   to find the average tobs
    max2 = session.query(Measurement.tobs, Measurement.date, func.max(Measurement.tobs)).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2010-01-01').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= '2017-08-23').all()
    session.close()

    max2 = [{"Date": max2[0][1], "Maximum": max2[0][0]}]

    return jsonify(min2,avg2,max2)

if __name__ == "__main__":
    app.run(debug=True)
