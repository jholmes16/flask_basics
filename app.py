from flask import Flask, jsonify,request

app = Flask(__name__)

@app.route('/')
def index():
    #What you put in name will appear on screen
    return '<h1>Hello</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    return '<h1>Hello {} you are on the home page!</h1>'.format(name)

@app.route('/json')
def json():
    return jsonify({'key' : 'value', 'listkey' : [1, 2, 3]})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}.  You are from {}.  You are on the query page!</h1>'.format(name, location)

if __name__ == "__main__":
    app.run(debug=True)
