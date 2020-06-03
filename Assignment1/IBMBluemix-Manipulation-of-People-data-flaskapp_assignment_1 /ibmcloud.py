import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')


conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=;PORT=50000;PROTOCOL=TCPIP;UID=;PWD=;", "", "")
 #Enter the host name userid and password---deleted for security purposes
# get service information if on IBM Cloud Platform
print("Connected to db")

if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]

else:
    raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def getdata():
    listofdata = []
    query_1 = "SELECT * FROM PEOPLE1"
    stmt_1 = ibm_db.exec_immediate(conn, query_1)
    result1 = ibm_db.fetch_both(stmt_1)
    while result1:
        listofdata.append(result1)
        result1 = ibm_db.fetch_both(stmt_1)

    return render_template('main.html', table=listofdata)

# Search for Harshit (Name) and show his picture on a web page.

@app.route("/show", methods=["POST", "GET"])
def show():
    name = request.form.get("name")
    query_1 = "SELECT PICTURE FROM PEOPLE1 WHERE NAME = '" + str(name) + "'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    result1 = ibm_db.fetch_both(stmt_11)
    while result1:
        photo = result1[0]
        result1 = ibm_db.fetch_both(stmt_11)

    return render_template('show.html', filename=photo, name=name, title='Show')

# Search for (display) all pictures where the salary is less than 99000.

@app.route("/lessthan", methods=["POST", "GET"])
def lessthan():
    range1 = request.form.get("range1")
    # range2 = request.form.get("range2")
    less_data = []
    query_1 = "SELECT PICTURE FROM PEOPLE1 WHERE SALARY < '" + str(range1) + "'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    result1 = ibm_db.fetch_both(stmt_11)
    while result1:
        less_data.append(result1)
        result1 = ibm_db.fetch_both(stmt_11)

    return render_template('lessthan.html', table=less_data, title='Less Than')

# Add a picture for Dave

@app.route("/insert", methods=["POST", "GET"])
def insert():
    pid = request.form.get("pid")
    file = request.form['file']
    query_1 = "UPDATE PEOPLE1 SET PICTURE = '" + str(file) + "' WHERE ID = '" + str(pid) + "'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    print(stmt_11)

    return render_template('insert.html', filename=file, title='Add/Insert')

# Remove Dave

@app.route("/delete", methods=["POST", "GET"])
def delete():
    dname = request.form.get("dname")
    pid = request.form.get("pid")
    deleted_data = []
    query_1 = "DELETE FROM PEOPLE1 WHERE ID = '" + str(pid) + "' AND NAME = '" + str(dname)+"'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    # result1 = ibm_db.fetch_both(stmt_11)
    query2 = "SELECT * FROM PEOPLE1"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result1 = ibm_db.fetch_both(stmt2)
    while result1:
        deleted_data.append(result1)
        result1 = ibm_db.fetch_both(stmt2)

    return render_template('delete.html', table=deleted_data, title='Delete')

# Change Dhruvi’s keywords to “Not so nice anymore”

@app.route("/update", methods=["POST", "GET"])
def update():
    kword = request.form.get("keywords")
    pid = request.form.get("pid")
    kword_data = []
    query_1 = "UPDATE PEOPLE1 SET KEYWORDS = '" + str(kword) + "' WHERE ID = '"+ str(pid)+ "'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    print("update: ", stmt_11)
    query2 = "SELECT * FROM PEOPLE1"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result1 = ibm_db.fetch_both(stmt2)
    while result1:
        kword_data.append(result1)
        result1 = ibm_db.fetch_both(stmt2)

    return render_template('update.html', table=kword_data, title='Update')

# Change Someone’s salary

@app.route("/updatesalary", methods=["POST", "GET"])
def updatesalary():
    range1 = request.form.get("range1")
    pid = request.form.get("pid")
    kword_data = []
    query_1 = "UPDATE PEOPLE1 SET SALARY = '" + str(range1) + "' WHERE ID = '"+ str(pid)+ "'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    print("update: ", stmt_11)
    query2 = "SELECT * FROM PEOPLE1"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result1 = ibm_db.fetch_both(stmt2)
    while result1:
        kword_data.append(result1)
        result1 = ibm_db.fetch_both(stmt2)

    return render_template('updatesalary.html', table=kword_data, title='UpdateSalary')

# find salary within a range

@app.route("/withinrange", methods=["POST", "GET"])
def withinrange():
    range1 = request.form.get("range1")
    range2 = request.form.get("range2")
    range_data = []
    query_1 = "SELECT * FROM PEOPLE1 WHERE SALARY BETWEEN '" + str(range1) + "' AND '" + str(range2)+"'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    result1 = ibm_db.fetch_both(stmt_11)
    while result1:
        range_data.append(result1)
        result1 = ibm_db.fetch_both(stmt_11)

    return render_template('withinrange.html', table=range_data, title='Within Range')


# find salary which is greater than

@app.route("/greaterthan", methods=["POST", "GET"])
def greaterthan():
    range1 = request.form.get("range1")
    # range2 = request.form.get("range2")
    greater_data = []
    query_1 = "SELECT * FROM PEOPLE1 WHERE SALARY > '" + str(range1) + "'"
    stmt_11 = ibm_db.exec_immediate(conn, query_1)
    result1 = ibm_db.fetch_both(stmt_11)
    while result1:
        greater_data.append(result1)
        result1 = ibm_db.fetch_both(stmt_11)

    return render_template('greaterthan.html', table=greater_data, title='Greater Than')



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
