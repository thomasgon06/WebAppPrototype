from flask import Blueprint, render_template, request, jsonify
import os
import datetime
import random
import json
from pymongo import MongoClient
from datetime import datetime
from flask import Flask, send_file


connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
current_db = client.SensorData

views = Blueprint('views', __name__)

@views.route('/')
def home():
   return render_template("index.html")

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

@views.route('/graph')
def returngraph():
    return render_template("graph.html")

@views.route('/entermodule')
def entermodule():
    return render_template("entermodule.html")

@views.route('/house')
def returnimage():
    return send_file('images/home.png', mimetype='image/png')

@views.route('/icon')
def returnicon():
    return send_file('images/icon.png', mimetype='image/png')


@views.route('/misbehaving')
def misbehaving():
    collection = current_db.SensorInfo
    meta = current_db.Metadata

    metacollec = meta.find()
    for m in metacollec:
        mostrecent = m["Most Recent"]
    startofrange = mostrecent.replace(hour=0, minute=0, second=0, microsecond=0)
    endofrange = mostrecent.replace(hour=23, minute=59, second=59, microsecond=999999)

    badtemps = list(collection.find({"Temperature": {"$not": {"$gte": 18, "$lte": 28}}, "Date Recorded" : {'$gte': startofrange,'$lte': endofrange}},{'_id': 0}).sort('Date Recorded', -1))
    badvoltages = list(collection.find({"Voltage": {"$not": {"$gte": 1000, "$lte": 1400}}, "Date Recorded" : {'$gte': startofrange,'$lte': endofrange}},{'_id': 0}).sort('Date Recorded', -1))
    badadc = list(collection.find({"ADC": {"$not": {"$gte": 1200, "$lte": 1250}}, "Date Recorded" : {'$gte': startofrange,'$lte': endofrange}},{'_id': 0}).sort('Date Recorded', -1))

    combined = badtemps + badvoltages + badadc
    docs = []
    [docs.append(x) for x in combined if x not in docs]
    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')
    return render_template('results.html', docs=docs)


@views.route('/alldata')
def alldata():
    
    collection = current_db.SensorInfo

    docs = list(collection.find({}, {'_id': 0}).sort('Date Recorded', -1))

    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')

  
    return render_template("results.html", docs = docs)


@views.route('/process_date', methods=['POST'])
def process_datet():
    datetime_string = request.form['datepicker']
    datetime_object = datetime.strptime(datetime_string, "%B %d %Y")
   

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
   
    datetime_object = datetime.strptime(datetime_string, '%B %d %Y %I:%M %p')

    collection = current_db.SensorInfo

    micro = mili * 1000
    requestedtime = datetime_object.replace(second=sec, microsecond=micro)

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
    first_datetime_object = datetime.strptime(first_datetime_string, '%B %d %Y %I:%M %p')
    starttime = first_datetime_object.replace(second=sec, microsecond=micro)

    second_datetime_string = request.form['datetimepicker2']
    sec2 = int(request.form['secondInput2'])
    mili2 = int(request.form['miliInput2'])
    micro2 = mili2 * 1000
    second_datetime_object = datetime.strptime(second_datetime_string, '%B %d %Y %I:%M %p')
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

@views.route('/data', methods=['POST'])
def getgraphdata():
   
   meta = current_db.Metadata
   collection = current_db.SensorInfo
   
   ModuleNumber = int(request.form["moduleInput"])
   

   metacollec = meta.find()
   for m in metacollec:
    mostrecent = m["Most Recent"]

    startofrange = mostrecent.replace(hour=0, minute=0, second=0, microsecond=0)
    endofrange = mostrecent.replace(hour=23, minute=59, second=59, microsecond=999999)

    docs = list(collection.find({ "Module #" : ModuleNumber, "Date Recorded" : {'$gte': startofrange,'$lte': endofrange}}, {'_id': 0}).sort('Date Recorded', -1))
    for doc in docs:
        if 'Date Recorded' in doc:  
            doc['Date Recorded'] = doc['Date Recorded'].strftime('%m/%d/%Y %I:%M:%S.%f %p')
    d = []
    r = []

    for doc in docs:
        d.append(doc.get("Date Recorded"))
        r.append(doc.get("Voltage"))

    domain = json.dumps(d)
    range = json.dumps(r)
    mostrecent = mostrecent.date().strftime("%B %d, %Y")

    return render_template("graph.html", domain=domain, range=range, ModuleNumber = ModuleNumber, mostrecent = mostrecent)
   
    




   



    