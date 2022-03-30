from flask import Flask, jsonify,request, url_for, redirect, session

app = Flask(__name__)

#configuration values link https://flask.palletsprojects.com/en/2.1.x/config/
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecret!' #needed for sessions to store data

@app.route('/')
def index():
    session.pop('name', None) #Removes session
    #What you put in name will appear on screen
    return '<h1>Hello</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return '<h1>Hello {} you are on the home page!</h1>'.format(name)

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
        return  '''<form method="POST" action="/theform">
                    <input type="text" name="name">
                    <input type="text" name="location">
                    <input type="submit" value="Submit">
                </form>'''
    else:
        name = request.form['name']
        location = request.form['location']
        return redirect(url_for('home', name=name, location=location))

@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']

    randomlist = data['randomlist']

    return jsonify({'result' : 'Success!', 'name' : name, 'location' : location, 'randomkeyinlist' : randomlist[1]})

if __name__ == "__main__":
    app.run()
