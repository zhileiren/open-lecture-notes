#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def root():
    return redirect("index")
@app.route("/index")
def index():
    return """\
            <html>
                <body>
                    <p> This is the index page</p>
                </body>
            </html>"""

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name="anonymous"):
    conn = sqlite3.connect("application.db")
    cursor = conn.cursor()
    results = list(cursor.execute("select * from students"))
    conn.close()
    return render_template("hello.html", name=name, results=results)



