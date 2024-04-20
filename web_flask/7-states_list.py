#!/usr/bin/python3
"""Starts a Flask web application."""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def tear_down(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def list_states():
    """
    Displays an HTML page with a list of all State objects in DBStorage.
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
