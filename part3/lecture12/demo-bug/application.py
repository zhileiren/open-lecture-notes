#!/usr/bin/python3

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
con = sqlite3.connect("rcbugs.db")
cursor = con.cursor()
results = list(cursor.execute("select package, maintainer, bugs from rcbugs"))

@app.route("/")
def index():
    return render_template("index.html", results=results)


