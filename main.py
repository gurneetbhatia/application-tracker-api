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

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == "GET":
        return data
    elif request.method == "POST":
        # id of the user should be generated here
        id = str(max(list(map(int, data))) + 1)
        content = request.get_json(silent=True)
        if 'name' in content and 'applications' in content:
            name = content.get('name')
            applications = content.get('applications')
            new_user = {id: {'id': id, 'name': name, 'applications': applications}}
            data.update(new_user)
            updateJson()
            return new_user
        else:
            # unprocessable entity
            return {}, 422


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    return (data[id], 200) if id in data else ("404", 404)

@app.route('/users/<id>/applications', methods=['GET'])
def get_user_applications(id):
    return (data[id]['applications'], 200) if id in data else ("404", 404)

def refreshData():
    data = json.load(open('data.json'))

def updateJson():
    json.dump(data, open('data.json', 'w'))
    #print(data)

app.run()
