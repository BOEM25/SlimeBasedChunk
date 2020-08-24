from flask import Flask, jsonify, request
from ilog import console
import json

app = Flask(__name__)

current = 6376913898527617522
step_size = 20000000000000
maxX = 18446744073709552000
fhinished = 0


@app.route("/heartbeat")
def heartbeat():
    return "200", 200


@app.route("/seeds", methods=['POST'])
def working_seeds():
    data = request.get_json()
    try:

        with open('data/seeds.json', 'r') as f:
            seedFile = json.load(f)
            f.close()
        seedList = list(seedFile['seeds'])

        for i in data['seeds']:
            seedList.append(i)

        with open('data/seeds.json', 'w') as f:
            seedFile['seeds'] = seedList
            json.dump(seedFile, f, indent=4)
            f.close()

        return "cool", 200
    except Exception as e:
        print(e)
        return "error", 400


doneData = {
    "set": id,
    "state": True
}


@app.route("/done", methods=['POST'])
def done():
    data = request.get_json()
    if data['state'] == True:
        console.log(f'id')


@app.route("/id", methods=['GET'])
def get_id():
    with open('data/ids.json', 'r') as f:
        ids = json.load(f)
        f.close()


@app.route("/state", methods=['GET'])
def give_state():
    global maxX, current, step_size
    global fhinished

    with open('data/ids.json', 'r') as f:
        ids = json.load(f)
        f.close()

    id = list(ids['ids'])

    highest = max(id)
    id.append(highest + 1)

    seedRange = current + step_size

    if seedRange >= maxX:

        if fhinished > 0:
            console.log("Complete")
            return "done", 123

        fhinished = 1
        seedRange = maxX

    x = {
        "seedMin": current + 1,
        "seedMax": seedRange,
        "x": [1, 3, 4, 5, 1, 3, 2, 9, 10],
        "z": [2, 2, 0, 5, 4, 6, 6, 5, 7],
        "set": highest + 1
        # gives and id to the current set which is later check when done is called and that saves it so can later check if this set is completed
    }

    current = seedRange
    with open('data/ids.json', 'w') as f:
        ids['ids'] = id
        json.dump(ids, f, indent=4)
        f.close()

    return jsonify(x), 200


@app.route("/process_json", methods=['POST'])
def processjson():
    data = request.get_json()
    return jsonify(data)


x = {
    "name": "bob",
    "array": ['one', 'two']
}

# First GET /state is called to get data, then the node does its calculations, then POST /done and  POST /seeds(with the found seeds and id) then starts again at POST /state

app.run(host='0.0.0.0', debug=True)
