#!/usr/bin/python3
"""Starts a Flask web application."""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def tear_down(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def states_and_cities():
    """Displays an HTML page with a list of all states and related cities."""
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
