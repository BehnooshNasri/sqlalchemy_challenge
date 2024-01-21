# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import pandas as pd

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
# Retrieve the most recent date
latest_date = session.query(func.max(Measurement.date)).scalar()
latest_date = pd.to_datetime(latest_date)

# Calculate one year ago from the most recent date
one_year_ago = latest_date - pd.DateOffset(days=365)

# Convert one_year_ago to a string
one_year_ago_str = one_year_ago.strftime("%Y-%m-%d")

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def homepage():
    """List all available routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start&gt; (replace &lt;start&gt; with an actual start date in 'YYYY-MM-DD' format)<br/>"
        "/api/v1.0/&lt;start&gt;/&lt;end&gt; (replace &lt;start&gt; and &lt;end&gt; with actual start and end dates in 'YYYY-MM-DD' format)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data as JSON."""

    # Query precipitation data for the last 12 months
    precipitation_data = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= one_year_ago_str)
        .all()
    )

    session.close()

    # Convert the results to a dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations."""
    # Query all stations
    station_results = session.query(Station.station).all()

    session.close()

    # Convert the results to a list
    stations_list = [station for station, in station_results]

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    # Retrieve the most active station ID
    most_active_station_id = (
        session.query(Measurement.station)
        .group_by(Measurement.station)
        .order_by(func.count().desc())
        .first()
        .station
    )

    # Retrieve the last 12 months of temperature observations for the most active station
    temperature_data = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == most_active_station_id)
        .filter(Measurement.date >= one_year_ago_str)
        .all()
    )

    session.close()

    # Convert the results to a list of dictionaries
    temperature_list = [{"date": date, "tobs": tobs} for date, tobs in temperature_data]

    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date."""
    # Perform calculations for TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    temperature_stats = (
        session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
        .filter(Measurement.date >= start)
        .all()
    )

    session.close()

    # Convert the results to a dictionary
    temp_stats_dict = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }

    return jsonify(temp_stats_dict)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range."""
    # Perform calculations for TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive
    temperature_stats = (
        session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )

    session.close()

    # Convert the results to a dictionary
    temp_stats_dict = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }

    return jsonify(temp_stats_dict)

# Run the app if this script is the main module
if __name__ == "__main__":
    app.run(debug=True)
