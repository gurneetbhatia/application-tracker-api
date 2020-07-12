from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.config["DEBUG"] = True

data = json.load(open('data.json'))

@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>API for Application Tracker</h1>
    <p>Made by <a href="https://github.com/gurneetbhatia">Gurneet Bhatia</a></p>
    '''

@app.route('/users')
def get_users():
    return data

@app.route('/users/<id>')
def get_user(id):
    return (data[id], 200) if id in data else ("404", 404)

app.run()
