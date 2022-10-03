from flask import Flask, render_template, request, redirect, url_for
import pymysql

con=None
cur=None

app=Flask(__name__)

def connectToDb():
    global con, cur
    con=pymysql.connect(host="localhost", user="root", passwd="", database="pydbcon")
    cur=con.cursor()
def disconnectDB():
    cur.close()
    con.close()
def getAllPersonData():
    connectToDb()
    selectquery="SELECT * FROM person;"
    cur.execute(selectquery)
    data=cur.fetchall()
    disconnectDB()
    return data
def insertToPersonTable(name, mobile, email, city, dob=None):
    try:
        connectToDb()
        insertQuery = "INSERT INTO person (name, mobile, email, city, DOB) VALUES (%s, %s, %s, %s, %s);"
        cur.execute(insertQuery, (name, mobile, email, city, dob))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False
def getOnePerson(person_id):
    connectToDb()
    selectquery = "SELECT * FROM person WHERE person_id=%s;"
    cur.execute(selectquery, (person_id, ))
    data = cur.fetchone()
    disconnectDB()
    return data
def updatePersonToTable(name, mobile, email, city, person_id, dob=None):
    try:
        connectToDb()
        updateQuery = "UPDATE person SET name=%s, mobile=%s, email=%s, city=%s,DOB=%s WHERE person_id=%s;"
        cur.execute(updateQuery, (name, mobile, email, city, dob, person_id))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False
def deletePersonFromTable(person_id):
    try:
        connectToDb()
        deleteQuery = "DELETE FROM person WHERE person_id=%s;"
        cur.execute(deleteQuery, (person_id))
        con.commit()
        disconnectDB()
        return True
    except:
        disconnectDB()
        return False

@app.route("/")
@app.route("/index/")
def index():
    #return "<h1>Flask Programming!<h1>"
    #data is tuple of tuples
    data=getAllPersonData()
    return render_template("index.html", data=data)
@app.route("/add/", methods=['GET', 'POST'])
def addPerson():
    if request.method == "POST":
        data = request.form
        if insertToPersonTable(data['txtName'], data['txtMobile'], data['txtEmail'], data['txtCity'], data['txtDOB']):
            message = "Record inserted Successfully."
        else:
            message = "Due to some issues couldn't insert record"
        return render_template("insert.html", message=message)
    return render_template("insert.html")

@app.route("/edit/", methods=['GET', 'POST'])
def updatePerson():
    person_id = request.args.get('id', type=int, default=1)
    data = getOnePerson(person_id)
    if request.method == "POST":
        fdata = request.form
        # print(fdata)
        if updatePersonToTable(fdata['txtName'], fdata['txtMobile'], fdata['txtEmail'], fdata['txtCity'], person_id, fdata['txtDOB']):
            message = "Record updated Successfully."
        else:
            message = "Due to some issues couldn't update record"
        return render_template("update.html", message=message)
    return render_template("update.html", data=data)

@app.route("/delete/")
def deletePerson():
    pass
    person_id = request.args.get('id', type=int, default=1)
    deletePersonFromTable(person_id)
    return redirect(url_for("index"))
if __name__=='__main__':
    app.run(debug=True)