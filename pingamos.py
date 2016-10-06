from flask import Flask, request, make_response
import sqlite3
from os.path import isfile
import json

def connect_db(dbname):
    db_is_created = isfile(dbname)
    connection = sqlite3.connect('pingamos.db')
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute("CREATE TABLE pings (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, lat INTEGER, lng INTEGER);")
        cursor.execute("CREATE TABLE users (id TEXT PRIMARY KEY);")
        connection.commit()
    return connection, cursor

app = Flask(__name__)

@app.route("/registerid/<string:id>", methods=["POST"])
def registerid(id):
    conn, cursor = connect_db("pingamos.db")
    pedido = json.loads(request.data)
    cursor.execute("INSERT INTO users('id') VALUES(" + id  + ");")
    conn.commit()

    ### METER RESPONSE CASO DÊ COCÓ ###

if __name__ == '__main__':
    conn, cursor = connect_db('pingamos.db')
    app.run(debug=True)
