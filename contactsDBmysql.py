from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import flask_restful

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'flask_practice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/contacts', methods=['GET'])
def getAll():
    con = mysql.connect()
    cur = con.cursor()
    query_string = "select * from flask_practice.contacts"

    cur.execute(query_string)
    con.close()

    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]

    return jsonify({'Contacts' : r})

@app.route('/contacts/<name>', methods=['GET'])
def getByName(name):
    con = mysql.connect()
    cur = con.cursor()
    query_string = "select * from flask_practice.contacts where contacts.name like '%{}%'".format(name)

    cur.execute(query_string)
    con.close()

    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]

    return jsonify({'Contacts' : r})

@app.route('/contacts/id/<id>', methods=['GET'])
def getById(id):
    con = mysql.connect()
    cur = con.cursor()
    query_string = "select * from flask_practice.contacts where contacts.id = '{}'".format(id)

    cur.execute(query_string)
    con.close()

    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]

    return jsonify({'Contacts' : r})

@app.route('/contacts', methods=['POST'])
def createContact():
    contactData = request.get_json()
    contactDict = dict(contactData['Contacts'])
    name = contactDict.get('name')
    phone = contactDict.get('phone_number')
    email = contactDict.get('email')
    con = mysql.connect()
    cur = con.cursor()
    query_string = "INSERT INTO flask_practice.contacts (name, phone_number, email) VALUES ('{}', '{}', '{}')".format(name, phone, email)

    print(query_string)
    cur.execute(query_string)
    con.commit()
    con.close()

    return getByName(name), 'ok'

@app.route('/contacts/id/<id>', methods=['PUT'])
def updateContact(id):
    contactData = request.get_json()
    contactDict = dict(contactData['Contacts'])
    name = contactDict.get('name')
    phone = contactDict.get('phone_number')
    email = contactDict.get('email')
    con = mysql.connect()
    cur = con.cursor()

    query_string = "UPDATE flask_practice.contacts SET name = '{}', phone_number = '{}', email = '{}' WHERE id = '{}'".format(name, phone, email, id)
    print(query_string)
    cur.execute(query_string)
    con.commit()
    con.close()

    return getByName(name), 'ok'

@app.route('/contacts/id/<id>', methods=['DELETE'])
def deleteContact(id):
    con = mysql.connect()
    cur = con.cursor()
    query_string = "DELETE FROM flask_practice.contacts WHERE id = '{}'".format(id)

    print(query_string)
    cur.execute(query_string)
    con.commit()
    con.close()

    return getById(id), 'ok'

if __name__ == '__main__':
    app.run(debug=True)
