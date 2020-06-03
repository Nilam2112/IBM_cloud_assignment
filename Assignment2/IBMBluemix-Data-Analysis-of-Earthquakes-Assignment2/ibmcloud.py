import os
from flask import Flask, redirect, render_template, request
import json
import geopy.distance
import ibm_db
import os
import datetime
import math

from math import radians, cos, sin, asin, sqrt, atan2

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
    # listofdata = []
    # query1 = "SELECT * FROM ALL_MONTH LIMIT 5"
    # stmt = ibm_db.exec_immediate(conn, query1)
    # result = ibm_db.fetch_both(stmt)
    # while result:
    #     listofdata.append(result)
    #     result = ibm_db.fetch_both(stmt)

    return render_template('main.html')

# @app.route("/upload", methods=["POST", "GET"])
# def upload():
#      # if request.method == 'POST':
#      #    con = sql.connect("database.db")
#      #    csv = request.files['myfile']
#      #    file = pd.read_csv(csv)
#      #    file.to_sql('ALL_MONTH', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
#      #    con.close()
    
    
#     upload_data = []
#     query1 = "SELECT COUNT(*) AS TOTAL, MIN(MAG) AS MINMAG, PLACE, LATITUDE, LONGITUDE FROM ALL_MONTH GROUP BY LATITUDE,LONGITUDE,PLACE HAVING MIN(MAG) > '2'"
#     stmt1 = ibm_db.exec_immediate(conn, query1)
#     result = ibm_db.fetch_both(stmt1)
#     while result:
#         upload_data.append(result)
#         result = ibm_db.fetch_both(stmt1)

#     return render_template('upload.html', table=upload_data, rowcount=len(upload_data), title='Upload data')

@app.route('/mag_greater', methods=['POST'])
def mag_greater():
    mag_1 = request.form['mag_1']
    Query_1 = 'select * from QUAKES where "MAG" > ' + mag_1
    select_Stmt = ibm_db.exec_immediate(conn, Query_1)
    rows = []
    count = 0
    result = ibm_db.fetch_assoc(select_Stmt)
    while result != False:
        count = count + 1
        rows.append(result.copy())
        result = ibm_db.fetch_assoc(select_Stmt)
    return render_template('mag_greater.html', rows=rows, count=count)

@app.route('/mag_range', methods=['POST'])
def mag_range():
    magto = request.form['magto']
    magfrom = request.form['magfrom']
    #Query_1 = 'select * from QUAKES where "TYPE" = \'earthquake\' and "MAG" >= ' + magto + ' and "MAG" <= ' + magfrom
    Query_1 = 'select * from QUAKES where "MAG" >= ' + magto + ' and "MAG" <= ' + magfrom
    select_Stmt = ibm_db.exec_immediate(conn, Query_1)
    rows = []
    count = 0
    result = ibm_db.fetch_assoc(select_Stmt)
    while result != False:
        count = count + 1
        rows.append(result.copy())
        result = ibm_db.fetch_assoc(select_Stmt)
    return render_template('mag_range.html', rows=rows, count=count)

@app.route('/searchwithradius',methods=['GET','POST'])

def searchwithradius(latitude=None,longitude=None,radius=None):
    try:
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        radius = float(request.form['radius'])

        lat1 = latitude - (radius / 69)
        lat2 = latitude + (radius / 69)
        long1 = longitude - (radius / 69)
        long2 = longitude + (radius / 69)


        Query_1="select * from QUAKES where \"LATITUDE\" > ? and \"LATITUDE\" < ? and \"LONGITUDE\" > ? and \"LONGITUDE\" < ? "

        select_Stmt = ibm_db.prepare(conn, Query_1)
        ibm_db.bind_param(select_Stmt, 1, str(lat1))
        ibm_db.bind_param(select_Stmt, 2, str(lat2))
        ibm_db.bind_param(select_Stmt, 3, str(long1))
        ibm_db.bind_param(select_Stmt, 4, str(long2))

        ibm_db.execute(select_Stmt)
        row=[]

        result = ibm_db.fetch_assoc(select_Stmt)

        while result:
            row.append(result)
            result = ibm_db.fetch_assoc(select_Stmt)
        return render_template('searchwithradius.html', row=row)

    except:
        # print "Exception Occured in Display Method"
        return render_template("main.html")


@app.route('/searchwithdistance',methods=['GET','POST'])
def searchwithdistance():
    lat = request.form['lat']
    long = request.form['long']
    dist = request.form['dist']

    Query_1 = 'select * from QUAKES'
    Stmt_1 = ibm_db.exec_immediate(conn, Query_1)
    oldrows = []
    rows = []
    count = 0
    radius = 6373.0
    result = ibm_db.fetch_assoc(Stmt_1)
    while result != False:
        oldrows.append(result.copy())
        result = ibm_db.fetch_assoc(Stmt_1)
    for row in oldrows:
        lat1 = math.radians(float(lat))
        lon1 = math.radians(float(long))
        lat2 = math.radians(float(row['LATITUDE']))
        lon2 = math.radians(float(row['LONGITUDE']))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        d = radius * c

        if(d < float(dist)):
            count = count+1
            rows.append(row)

    return render_template('searchwithdistance.html', rows=rows,count=count)

@app.route('/closestearthqithMag',methods=['GET','POST'])
def closestearthqithMag():
    lat = request.form['lat']
    long = request.form['long']
    dist = request.form['dist']
    mag = request.form['mag']
    Query_1 = 'select * from QUAKES where "MAG" > ' + mag
    Stmt_1 = ibm_db.exec_immediate(conn, Query_1)
    oldrows = []
    rows = []
    count = 0
    radius = 6373.0
    result = ibm_db.fetch_assoc(Stmt_1)
    while result != False:
        oldrows.append(result.copy())
        result = ibm_db.fetch_assoc(Stmt_1)
    for row in oldrows:
        lat1 = math.radians(float(lat))
        lon1 = math.radians(float(long))
        lat2 = math.radians(float(row['LATITUDE']))
        lon2 = math.radians(float(row['LONGITUDE']))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        d = radius * c

        if(d < float(dist)):
            count = count+1
            rows.append(row)

    return render_template('closestearthqithMag.html', rows=rows,count=count)

@app.route('/daterangemag', methods=['POST'])
def daterangemag():
    startdate = request.form['startdate']
    enddate = request.form['enddate']
    magto = request.form['magto']
    magfrom = request.form['magfrom']
    Query_1 = 'select * from QUAKES where  "TIME" >= \'' + startdate + '\' and "TIME" <= \'' + enddate + '\' and "MAG" >= ' + magto + ' and "MAG" <= ' + magfrom    # selectQuery = 'select * from QUAKES where "type" = \'earthquake\' and "time" >= \'' + sdate + '\' and "time" <= \'' + edate + '\' and "mag" >= ' + smag + ' and "mag" <= ' + emag
    Stmt_1 = ibm_db.exec_immediate(conn, Query_1)
    rows = []
    count = 0
    result = ibm_db.fetch_assoc(Stmt_1)
    while result != False:
        count = count + 1
        rows.append(result.copy())
        result = ibm_db.fetch_assoc(Stmt_1)
    return render_template('daterangemag.html', rows=rows, count=count)

@app.route('/searchdistanceweek',methods=['GET','POST'])
def searchdistanceweek():
    lat = request.form['lat']
    long = request.form['long']
    dist = request.form['dist']
    startdate = request.form['startdate']
    enddate = request.form['enddate']

    Query_1 = 'select * from QUAKES  where  "TIME" >= \'' + startdate + '\' and "TIME" <= \'' + enddate + '\' ' + 'order by "MAG" DESC'
    Stmt_1 = ibm_db.exec_immediate(conn, Query_1)
    oldrows = []
    rows = []
    count = 0
    radius = 6373.0
    result = ibm_db.fetch_assoc(Stmt_1)
    while result != False:
        oldrows.append(result.copy())
        result = ibm_db.fetch_assoc(Stmt_1)
    for row in oldrows:
        lat1 = math.radians(float(lat))
        lon1 = math.radians(float(long))
        lat2 = math.radians(float(row['LATITUDE']))
        lon2 = math.radians(float(row['LONGITUDE']))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        d = radius * c

        if(d < float(dist)):
            count = count+1
            rows.append(row)

    return render_template('searchdistanceweek.html', rows=rows,count=count)

port = os.getenv('PORT', '5000')

if __name__ == '__main__':
    app.debug = True
    # app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))
