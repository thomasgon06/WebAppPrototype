
# Installation Instructions

1. Create a python virtual environment using the command `python -m venv myenv`, where `myenv` can be any name you choose.

2. Activate the virtual environment by using the command `myenv\Scripts\activate` on Windows or `source myenv/bin/activate` on Unix-based systems.

3. Install all of the required packages by running the command `pip install -r requirements.txt`. Note: this also includes all of the packages needed for the helper scripts and database script projects.

4. Download this project and the Helper Scripts Project.

5. Download and configure MongoDB using this [tutorial](https://www.mongodb.com/docs/manual/installation/).

6. Use MongoDB Compass to create a `SensorData` database with two collections, `Metadata` and `Sensorinfo`.

7. Use the Test data helper script to fill the database up.

8. Configure your firewall so that port 80 is open.

9. Navigate to the directory where the web app is, then run the command `gunicorn --bind 0.0.0.0:80 -k 'gthread' wsgi:app` to deploy it.
