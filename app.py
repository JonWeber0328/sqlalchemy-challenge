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

    # Query all dates and prcp measurements
    results = session.query(Station.name, Station.id, Station.station).all()
    session.close()

    return jsonify(results)



if __name__ == "__main__":
    app.run(debug=True)
