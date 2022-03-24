from distutils.log import debug
from flask import Flask, render_template, jsonify
from jinja2 import Template
import mysql.connector

app = Flask(__name__, static_url_path='')

#function to test url works
@app.route("/hello")
def hello():
   return "Hello world"

#function for the home page that shows the map
@app.route("/map")
def index():
    return render_template('Google_Maps.html')

#function that connects to database, queries the 'Station' table and returns the results as JSON
@app.route("/stations")
def station():
    #Connect to dBikes database.   'mycursor' used to execute database commands.
    mydb = mysql.connector.connect(
    host="dbbikes.cpwzqhmscagf.eu-west-1.rds.amazonaws.com",
    user="group20",
    password="30830Group20",
    database="dBikes")

    mycursor = mydb.cursor()    
    mycursor.execute("SELECT * FROM Station")
    myresult = mycursor.fetchall()
    response = jsonify(myresult)
    return response

#function that connects to database, queries the 'Bikes' table and returns the results as JSON
@app.route("/bikes/<stationName>")
def bikes(stationName):
    #Connect to dBikes database.   'mycursor' used to execute database commands.
    mydb = mysql.connector.connect(
    host="dbbikes.cpwzqhmscagf.eu-west-1.rds.amazonaws.com",
    user="group20",
    password="30830Group20",
    database="dBikes")

    query = """SELECT * FROM Bikes WHERE Address = %s ORDER BY Updated DESC LIMIT 1"""

    #put '/' back in station address for 'Princes Street / O'Connell Street' for the query
    x = stationName.replace("!", "/")

    tup = [x]
    
    mycursor = mydb.cursor()    
    mycursor.execute(query, tup)
    myresult = mycursor.fetchall()
    response = jsonify(myresult)
    return response

if __name__ == "__main__":
    app.run(debug=True)