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

@app.route('/users/<id>/applications', methods=['GET', 'POST'])
def get_user_applications(id):
    if request.method == "GET":
        return (data[id]['applications'], 200) if id in data else ("404", 404)
    elif request.method == "POST":
        if id not in data:
            return ("404", 404)
        else:
            # create a new application for this user
            print(data[id]['applications'])
            app_id = str(max(list(map(int, data[id]['applications']))) + 1)
            content = request.get_json(silent=True)
            if 'company' in content and 'position' in content and 'applicationStatus' in content and 'deadline' in content:
                # all the required data is present
                company = content.get('company')
                position = content.get('position')
                appStatus = content.get('applicationStatus')
                deadline = content.get('deadline')
                # notes are optional so handle them accordingly
                notes = content.get('notes') if 'notes' in content else []
                new_app = {
                    app_id: {
                        "company": company,
                        "position": position,
                        "applicationStatus": appStatus,
                        "deadline": deadline,
                        "notes": notes
                    }
                }
                data[id]['applications'].update(new_app)
                updateJson()
                return new_app
            else:
                # unprocessable entity
                return {}, 422

def refreshData():
    data = json.load(open('data.json'))

def updateJson():
    json.dump(data, open('data.json', 'w'))
    #print(data)

app.run()
