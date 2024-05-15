
# Web App Documentation

---

## Overview

This web app is a prototype designed to query a MongoDB database and retrieve sensor data based on various parameters such as date, time, voltage, and 
module number. 

## Software Stack
- Primary Programming Language: Python
- Database Managment System: MongoDB
- Web Framework: Flask
- Object-Docment Mapping Library: Pymongo
    
## Database Structure
- This web app is designed to work with a MongoDB database with two collections. The first is called "SensorInfo" and it is where the documents are
  stored. Additionally,there is an index placed on the documents’ Date Recorded attribute. Due to MongoDB databases being non-relational, the number and
  types of attributes each document has can vary. But, at the moment, each document has eight attributes. These attributes are: ID, Date Recorded, Mooring 
  Line, Module #, Photo Multiplier #, Voltage, temperature and ADC. The other collection is called "Metadata", this collection contains one document with 
  one attribute called Most Recent. It is used to keep track of what day and time data was last recorded. 

## External Tools Used

- **Pymongo**:
  - Pymongo is the Object-Document Mapping Library used to access the database. Its documentation can be found [here](https://pymongo.readthedocs.io/en/stable/).

- **Flask**:
    - Flask is the web framework that powers the application. Its documentation can be found [here](https://flask.palletsprojects.com/en/3.0.x/).
    
- **Gunicorn**:
    - Gunicorn is a Python WSGI HTTP server used to host the web application.  Its documentation can be found [here](https://docs.gunicorn.org/en/stable/).
    
- **Bootstrap 5.3**:
    - Bootstrap is a front-end framework used to style our web application and provide some interactivity. Its documentation can be found [here](https://getbootstrap.com/docs/5.3/getting-started/introduction/).
    
- **Flatpickr**:
    - Flatpicker is a date and time picker. Its documentation can be found [here](https://flatpickr.js.org/). 
    
- **Chart.js**:
    - Chatjs is a JavaScript library used for making charts. In this application, it is used to create voltage graphs. Its documentation can be found [here] (https://www.chartjs.org/docs/latest/getting-started/).


## File Structure

- **Root**:
  - `wsgi.py`: Entry point for deploying the web application on a WSGI server.

    - **Website**:
        - `__init__.py`: Initializes the website package.
        - `views.py`: Contains routes that handle requests and return responses.
        
    - **Images**:
        - `icon.png`
        - `home.png`
        
    - **Static**:
        - `styles.css`: Contains CSS styles for the website.
        - `scripts.js`: Contains JavaScript for the website.

    - **Templates**:
        - `base.html`: Base template containing common structure and layout.
        - `index.html`
        - `voltagerange.html`
        - `timerange.html`
        - `graph.html`
        - `results.html`
        - `dateselect.html`
        - `entermodule.html`
        - `voltage.html`
        - `exacttime.html`
---

## Routes and Queries

### 1. Home Page
- **Route**: `/`
- **Method**: GET
- **Description**: Renders the `index.html` template, serving as the homepage.
- **Returns**: `index.html`

### 2. Date Selection Page
- **Route**: `/dateselect`
- **Method**: GET
- **Description**: Renders the `dateselect.html` template for selecting a date.
- **Returns**: `dateselect.html`

### 3. Exact Time Selection Page
- **Route**: `/exacttime`
- **Method**: GET
- **Description**: Renders the `exacttime.html` template for selecting an exact time.
- **Returns**: `exacttime.html`

### 4. Time Range Selection Page
- **Route**: `/timerange`
- **Method**: GET
- **Description**: Renders the `timerange.html` template for selecting a time range.
- **Returns**: `timerange.html`

### 5. Voltage Page
- **Route**: `/voltage`
- **Method**: GET
- **Description**: Renders the `voltage.html` template for entering a voltage.
- **Returns**: `voltage.html`

### 6. Voltage Range Selection Page
- **Route**: `/voltagerange`
- **Method**: GET
- **Description**: Renders the `voltagerange.html` template for selecting a voltage range.
- **Returns**: `voltagerange.html`

### 7. Graph Page
- **Route**: `/graph`
- **Method**: GET
- **Description**: Renders the `graph.html` template to display a graph of a module's voltages.
- **Returns**: `graph.html`

### 8. Enter Module Page
- **Route**: `/entermodule`
- **Method**: GET
- **Description**: Renders the `entermodule.html` template for entering a module number.
- **Returns**: `entermodule.html`

### 9. House Icon
- **Route**: `/house`
- **Method**: GET
- **Description**: Fetches the house home icon.
- **Returns**: `images/home.png`

### 10. Icon
- **Route**: `/icon`
- **Method**: GET
- **Description**: Fetches the favicon.
- **Returns**: `images/icon.png`

### 11. Query for Misbehaving Sensors
- **Route**: `/misbehaving`
- **Method**: GET
- **Description**: Retrieves sensor data for documents that have a Date Recorded value that matches the metadata table and do not have a  temperature value within the range of 18-28°C, a voltage value within the range of 1000 to 1400, or an ADC value within the range of 1200 to 1250.
- **Database Collections**: `SensorInfo`, `Metadata`
**Parameters**:
  - none
- **Returns**: `results.html, docs=docs`

### 12. Query for all data
- **Route**: `/alldata`
- **Method**: POST
- **Description**: Retrieves all sensor data.
- **Database Collection**: `SensorInfo`
- **Parameters**:
  - none
- **Returns**: `results.html, docs=docs`

### 13. Query for Data by Date
- **Route**: `/process_date`
- **Method**: POST
- **Description**: Retrieves sensor data for a specific date.
- **Database Collection**: `SensorInfo`
- **Parameters**:
  - `datepicker` (date)
- **Returns**: `results.html, docs=docs`

### 14. Query for Data by Exact Time
- **Route**: `/process_exacttime`
- **Method**: POST
- **Description**: Retrieves sensor data for an exact time.
- **Database Collection**: `SensorInfo`
- **Parameters**:
  - `datetimepicker` (datetime)
  - `secondInput` (second)
  - `miliInput` (millisecond)
- **Returns**: `results.html, docs=docs`

### 15. Query for Data by Time Range
- **Route**: `/process_timerange`
- **Method**: POST
- **Description**: Retrieves sensor data within a specified time range.
- **Database Collection**: `SensorInfo`
- **Parameters**:
  - `datetimepicker` (datetime)
  - `secondInput` (second)
  - `miliInput` (millisecond)
  - `datetimepicker2` (datetime)
  - `secondInput2` (second)
  - `miliInput2` (millisecond)
- **Returns**: `results.html, docs=docs`

### 16. Query for Data by Voltage Range
- **Route**: `/findvoltage`
- **Method**: POST
- **Description**: Retrieves sensor data with a specified voltage.
- **Database Collection**: `SensorInfo`
- **Parameters**:
  - `voltageInput` (voltage)
- **Returns**: `results.html, docs=docs`

### 17. Query for Data by Voltage Range
- **Route**: `/findvoltagerange`
- **Method**: POST
- **Description**: Retrieves sensor data within a specified voltage range.
- **Database Collection**: `SensorInfo`
- **Parameters**:
  - `voltageInput` (start voltage)
  - `endvoltageInput` (end voltage)
- **Returns**: `results.html, docs=docs`

### 18. Query for Recent Graph Data by Module
- **Route**: `/data`
- **Method**: POST
- **Description**: Retrieves voltage data for a specific module number for the most recent day.
- **Database Collections**: `SensorInfo`, `Metadata`
- **Parameters**:
  - `moduleInput` (module number)
**Returns**: `"graph.html", domain=domain, range=range, ModuleNumber = ModuleNumber, mostrecent = mostrecent`

---

## Installation Instructions

1. Create a python virtual environment using the command `python -m venv myenv`, where `myenv` can be any name you choose.

2. Activate the virtual environment by using the command `myenv\Scripts\activate` on Windows or `source myenv/bin/activate` on Unix-based systems.

3. Install all of the required packages by running the command `pip install -r requirements.txt`. Note: this also includes all of the packages needed for the helper scripts and database script projects.

4. Download this project and the Helper Scripts Project.

5. Download and configure MongoDB using this [tutorial](https://www.mongodb.com/docs/manual/installation/).

6. Use MongoDB Compass to create a `SensorData` database with two collections, `Metadata` and `Sensorinfo`.

7. Use the Test data helper script to fill the database up.

8. Configure your firewall so that port 80 is open.

9. Navigate to the directory where the web app is, then run the command `gunicorn --bind 0.0.0.0:80 -k 'gthread' wsgi:app` to deploy it.

