from flask import Blueprint, render_template, request
import os
import datetime
import pprint
import random
import pprint
from pymongo import MongoClient
from datetime import datetime


connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
current_db = client.SensorData

views = Blueprint('views', __name__)

@views.route('/')
def home():
   return render_template("home.html")

@views.route('/dateselect')
def dateselect():
    return render_template("dateselect.html")

@views.route('/exacttime')
def timeselect():
    return render_template("exacttime.html")

@views.route('/timerange')
def timerange():
    return render_template("timerange.html")

@views.route('/voltage')
def voltage():
    return render_template("voltage.html")

@views.route('/voltagerange')
def voltagerange():
    return render_template("voltagerange.html")


@views.route('/results')
def results():
    
    collection = current_db.SensorInfo

    docs = list(collection.find({}, {'_id': 0}).sort('Date Recorded', -1))

    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')

  
    return render_template("results.html", docs = docs)


@views.route('/process_date', methods=['POST'])
def process_datet():
    datetime_string = request.form['datepicker']
    datetime_object = datetime.strptime(datetime_string, '%m/%d/%Y')

    collection = current_db.SensorInfo

    start_of_day = datetime_object.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = datetime_object.replace(hour=23, minute=59, second=59, microsecond=999999)

    docs = list(collection.find({ "Date Recorded" : {'$gte': start_of_day,'$lte': end_of_day} }, {'_id': 0}).sort('Date Recorded', -1))
    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')

    return render_template("results.html", docs = docs)


@views.route('/process_exacttime', methods=['POST'])
def process_exacttime():
    datetime_string = request.form['datetimepicker']
    sec = int(request.form['secondInput'])
    mili = int(request.form['miliInput'])
   
    datetime_object = datetime.strptime(datetime_string, '%m/%d/%Y %I:%M %p')

    collection = current_db.SensorInfo

    micro = mili * 1000
    requestedtime = datetime_object.replace(second=sec, microsecond=micro)
    print(requestedtime)

    docs = list(collection.find({ "Date Recorded" : requestedtime }, {'_id': 0}).sort('Date Recorded', -1))
    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')

    return render_template("results.html", docs = docs)

@views.route('/process_timerange', methods=['POST'])
def process_timerange():

    first_datetime_string = request.form['datetimepicker']
    sec = int(request.form['secondInput'])
    mili = int(request.form['miliInput'])
    micro = mili * 1000
    first_datetime_object = datetime.strptime(first_datetime_string, '%m/%d/%Y %I:%M %p')
    starttime = first_datetime_object.replace(second=sec, microsecond=micro)

    second_datetime_string = request.form['datetimepicker2']
    sec2 = int(request.form['secondInput2'])
    mili2 = int(request.form['miliInput2'])
    micro2 = mili2 * 1000
    second_datetime_object = datetime.strptime(second_datetime_string, '%m/%d/%Y %I:%M %p')
    endtime = second_datetime_object.replace(second=sec2, microsecond=micro2)


    collection = current_db.SensorInfo

    docs = list(collection.find({ "Date Recorded" : {'$gte': starttime,'$lte': endtime} }, {'_id': 0}).sort('Date Recorded', -1))
    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')

    return render_template("results.html", docs = docs)


@views.route('/findvoltage', methods=['POST'])
def findvoltage():

    voltage = float(request.form['voltageInput'])
   

    collection = current_db.SensorInfo

    docs = list(collection.find({ "Voltage" : voltage }, {'_id': 0}).sort('Date Recorded', -1))
    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')

    return render_template("results.html", docs = docs)


@views.route('/findvoltagerange', methods=['POST'])
def findvoltagerange():

    startvoltage = float(request.form['voltageInput'])
    endvoltage = float(request.form['endvoltageInput'])
   

    collection = current_db.SensorInfo

    docs = list(collection.find({ "Voltage" : {'$gte': startvoltage,'$lte': endvoltage} }, {'_id': 0}).sort('Date Recorded', -1))
    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')

    return render_template("results.html", docs = docs)
   
   
    




   



    