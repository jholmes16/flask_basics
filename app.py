from flask import Flask, jsonify,request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

#configuration values link https://flask.palletsprojects.com/en/2.1.x/config/
app.config['DEBUG'] = True #also auto reload screen on changes
app.config['SECRET_KEY'] = 'thisisasecret!' #needed for sessions to store data

def connect_db():
    sql = sqlite3.connect('C:/Users/JahmaulHolmes/Flask/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    session.pop('name', None) #Removes session
    #What you put in name will appear on screen
    return '<h1>Hello</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=True, \
    myList=['one', 'two', 'three', 'four'], listofdictionaries=[{'name' : 'Zach'}, {'name' : 'Zoey'}], results=results)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name'] #read the session name
    else:
        name = 'NotinSession'
    return jsonify({'key' : 'value', 'listkey' : [1, 2, 3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}.  You are from {}.  You are on the query page!</h1>'.format(name, location)

@app.route('/theform', methods=['GET', 'POST'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        return redirect(url_for('home', name=name, location=location))

@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']

    randomlist = data['randomlist']

    return jsonify({'result' : 'Success!', 'name' : name, 'location' : location, 'randomkeyinlist' : randomlist[1]})

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}.  The name is {}. The location is {}.</h1>'.format(results[2]['id'], results[2]['name'], results[2]['location'])

if __name__ == "__main__":
    app.run()
