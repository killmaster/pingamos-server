from flask import Flask, request, make_response
#from pyfcm import FCMNotification
import sqlite3
from os.path import isfile
import json
import os

# TODO check db connections

#push_service = FCMNotification(api_key=os.environ['FCM'])

def connect_db(dbname):
    db_is_created = isfile(dbname)
    connection = sqlite3.connect('pingamos.db')
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute("CREATE TABLE pings (id REAL PRIMARY KEY, name TEXT, lat REAL, lng REAL);")
        cursor.execute("CREATE TABLE users (id TEXT PRIMARY KEY);")
        connection.commit()
    return connection, cursor

app = Flask(__name__)

@app.route("/registerid", methods=["POST"])
def registerid():
    conn, cursor = connect_db("pingamos.db")
    userid = request.args.get('id')
    cursor.execute("INSERT INTO users('id') VALUES('" + userid  + "');")
    conn.commit()

    ### METER RESPONSE CASO DÊ COCÓ ###

@app.route("/ping", methods=["POST"])
def storeping():
    name = request.args.get('name')
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    conn, cursor = connect_db("pingamos.db")
    cursor.execute("INSERT INTO pings('name','lat','lng') VALUES('"+ name +"',"+ lat +","+ lng +");")
    conn.commit()
    # HERE BE DRAGONS
    # and untried code and APIs
    # proceed with caution
    # make unit tests for me please I want to sleep
    #cursor.execute("SELECT * FROM users;")
    # This should have a list with all the user ids
    #data = cursor.fetchall()
    # Now to get FCM to notify them all
    #message = {
    #        "name": name,
    #        "lat":  lat,
    #        "lng":  lng
    #        }
    #result = push_service.notify_multiple_devices(registration_ids=data, data_message=message)



@app.route("/pings", methods=["GET"])
def getpings():
    conn, cursor = connect_db("pingamos.db")
    # here we get all the pings from the database
    cursor.execute("SELECT * FROM pings;")
    # now we make a json object with all the data we got from the query
    data = cursor.fetchall()
    res = make_response(json.dumps(data))
    res.status_code = 200
    # and we send it back as a response
    return res

@app.route("/ping", methods=["GET"])
def getping():
    conn, cursor = connect_db("pingamos.db")
    # we get the id of the ping we want
    # to get the details from from the request
    pingid = int(request.args.get('id'))
    # now we query the db for that id
    cursor.execute("SELECT * FROM pings WHERE 'id' = " + pingid + ";")
    # time to dump all that sweet sweet data into a json
    data = cursor.fetchall()
    res = make_response(json.dumps(data))
    res.status_code = 200
    # and again we send it back as a response
    return res


if __name__ == '__main__':
    conn, cursor = connect_db('pingamos.db')
    app.run(host='0.0.0.0',debug=True)
