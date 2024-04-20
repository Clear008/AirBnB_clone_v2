#!/usr/bin/python3
"""Starts a Flask web application."""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def tear_down(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """Displays an HTML page with a list of all States."""
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def statesid(id):
    """Displays an HTML page with info about <id>, if it exists."""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
