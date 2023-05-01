# Import the dependencies.
import numpy as np
import datetime as dt
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:/Users/EmGre/OneDrive/Desktop/Class Repositories/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measurement = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#Create a home page with the available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YOUR DATE HERE <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        """Return a list of all precipitation from the last year"""


        # Query all preciptation
        prcp_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= dt.date(2016,8,23)).all()

        # Convert list of tuples into a callable dictionary
        all_prcp_data = []
        for date, prcp in prcp_data:
              prcp_dict = {}
              prcp_dict["Date"] = date
              prcp_dict["Precipitation"] = prcp
              all_prcp_data.append(prcp_dict)

        return jsonify(all_prcp_data)


@app.route("/api/v1.0/stations")
def stations():
        """Return a list of all active stations"""


        # Query all preciptation
        station_data = session.query(stations.station).all()

        # Convert list of tuples into a callable dictionary
        all_stations = list(np.ravel(station_data))

        return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
        """Return the dates and temperature observations of the most-active station for the previous year of data."""

        # Query all preciptation
        active_station_temps = session.query(measurement.date, measurement.tobs).filter(measurement.station == "USC00519281").\
            filter(measurement.date >= dt.date(2016,8,23)).all()

        # Convert list of tuples into a callable dictionary
        all_acive_data = []
        for date, temp in active_station_temps:
              active_temp_dict = {}
              active_temp_dict["Date"] = date
              active_temp_dict["Temperature"] = temp
              all_acive_data.append(active_temp_dict)

        return jsonify(all_acive_data)


#End Session
session.close()

if __name__ == '__main__':
      app.run(debug=True)