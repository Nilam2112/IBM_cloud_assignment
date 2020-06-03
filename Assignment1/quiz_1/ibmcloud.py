import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')

conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=;PORT=50000;PROTOCOL=TCPIP;UID=;PWD=;", "", "")
 #Enter the host name userid and password---deleted for security purposes
# get service information if on IBM Cloud Platform

print("Connected to db")  # Enter the host name userid and password---deleted for security purposes
# get service information if on IBM Cloud Platform
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]

else:
    raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def getdata():
    listofdata = []
    query1 = "SELECT * FROM DATA"
    stmt = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt)
    while result:
        listofdata.append(result)
        result = ibm_db.fetch_both(stmt)

    return render_template('main.html', table=listofdata)

@app.route("/show", methods=["POST", "GET"])
def show():
    name = request.form.get("name")
    query1 = "SELECT PIC FROM DATA WHERE NAME = '" + str(name) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        photo = result[0]
        result = ibm_db.fetch_both(stmt1)

    return render_template('show.html', filename=photo, name=name, title='Show')


    # find owner within a range

@app.route("/withinrange", methods=["POST", "GET"])
def withinrange():
    range1 = request.form.get("range1")
    range2 = request.form.get("range2")
    range_data = []
    query1 = "SELECT PIC,NAME FROM DATA WHERE OWNER BETWEEN '" + str(range1) + "' AND '" + str(range2)+"'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        range_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('withinrange.html', table=range_data, title='Within Range')

# Add a picture for Dave

@app.route("/insert", methods=["POST", "GET"])
def insert():
    name = request.form.get("name")
    file = request.form['file']
    query1 = "UPDATE DATA SET PIC = '" + str(file) + "' WHERE NAME = '" + str(name) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    print(stmt1)

    return render_template('insert.html', filename=file, title='Add/Insert')


@app.route("/tfile", methods=["POST", "GET"])
def tfile():
    file = request.form['file']
    # file1 = open("text.txt","r")     
    # if file1.mode == "r":
    #     contents =file1.read()
    #     print(contents)

    return render_template('tfile.html',filename=file, title='text file')

  
# @app.route("/")
# @app.route("/main")
# @app.route("/home")
# def main():
#     # return render_template('main.html', listofdata=listofdata, title='Home')
#     return render_template('main.html', title='Home')

port = os.getenv('PORT', '5000')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))
