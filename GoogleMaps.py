from distutils.log import debug
from flask import Flask, render_template, jsonify, make_response, request
from jinja2 import Template
import mysql.connector
import requests
import json
import pickle
from pickle import load
import joblib


app = Flask(__name__, static_url_path='')

#function to test url works
@app.route("/hello")
def hello():
    return render_template('test.html')

#function to test code
# @app.route("/test", methods=['POST'])
# def test():
#     # string
#     output = request.get_json()
#     print(type(output))
#     # dict
#     result = json.loads(output)
#     print(result)
#     print(type(result))
#     return result

#function to test code
@app.route("/")
def asd():
    print('hello')
    return render_template('test2.html')

#function for the home page that shows the map
@app.route("/map")
def index():
    stat = station().get_json()
    bikes = stations().get_json()
    return render_template('Google_Maps.html', stat = stat, bikes = bikes)

# function that loads a page with a list of stations
@app.route("/StationTable")
def index2():
    stat2 = stations().get_json()
    return render_template('table.html', stat = stat2)

# Function that queries most recent data from the dynamic station
@app.route("/stations2")
def stations():
    #Connect to dBikes database.   'mycursor' used to execute database commands.
    mydb = mysql.connector.connect(
    host="dbbikes.cpwzqhmscagf.eu-west-1.rds.amazonaws.com",
    user="group20",
    password="30830Group20",
    database="dBikes")

    mycursor = mydb.cursor()    
    mycursor.execute("SELECT DISTINCT * FROM Bikes INNER JOIN (SELECT DISTINCT(Address), MAX(Updated) AS Maxscore FROM Bikes GROUP BY Address) topscore ON Bikes.Address = topscore.Address AND Bikes.Updated = topscore.maxscore ORDER BY Bikes.Address ASC")

    myresult = mycursor.fetchall()
    response = jsonify(myresult)
    return response

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
    mycursor.execute("SELECT * FROM Station ORDER BY Address ASC")
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

    query = """SELECT * FROM Bikes WHERE Address = %s ORDER BY Updated DESC"""

    #put '/' back in station address for 'Princes Street / O'Connell Street' for the query
    statName = stationName.replace("!", "/")

    tup = [statName]
    
    mycursor = mydb.cursor()    
    mycursor.execute(query, tup)
    myresult = mycursor.fetchall()
    response = jsonify(myresult)
    return response


@app.route("/predict/<string:station1>/<int:days_test>/<int:hours_test>")
def predict(station1, days_test, hours_test):
    args = request.args
    #haven't included station name yet
    #print(args)
    #print(days_test)
    #print(type(args))
    print("Station_Name", station1)
    print("Days", days_test)
    print("hours:", hours_test)
    #print(args.get(days_test))
    #print(args.get('days_test'))
    #print("test", type(args))
    #print("hello")

    weekday = days_test
    hour_time = hours_test

    #handle = "'Charleville Road_model.pkl'"

    #joblib.load(filename, mmap_mode=None)

    #This works

    file_name = 'SoftEngPickle/' + station1 + "_model.pkl"

    new_file_name = file_name

    print("new_file_name", new_file_name)

    with open(new_file_name, 'rb') as f:


        model = joblib.load(f)
        
        bike_avail_predict = model.predict([[hour_time, weekday]])

        predict_list = bike_avail_predict.tolist()
        predict_dict = {"bikes": round(predict_list[0], 0)}
        result = json.dumps(predict_dict)
        print(type(result))
        print(result)
        return result

#CONOR DDED 2 DONE




if __name__ == "__main__":
    app.run(debug=True)