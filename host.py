from flask import Flask, jsonify, request
from ilog import console
import json

app = Flask(__name__)

current = 0
step_size = 200000000
max = 18446744073709552000
fhinished = 0

@app.route("/heartbeat")
def heartbeat():
    return "200", 200


@app.route("/seeds", methods=['POST'])
def working_seeds():
    listS = [0]
    data = request.get_json()
    try:
        for i in data['seeds']:
            #print(i)
            listS.append(i)
        console.log(listS)
        return "cool", 200
    except Exception as e:
        print(e)
        return "error", 400


@app.route("/state", methods=['GET'])
def give_state():
    global max, current, step_size
    global fhinished
    seedRange = current + step_size
    if seedRange >= max:

        if fhinished > 0:
            console.log("Complete")
            return "done"
        fhinished = 1
        seedRange = max

    x = {
        "seedMin": current + 1,
        "seedMax": seedRange
    }
    current = seedRange
    return jsonify(x), 200


@app.route("/process_json", methods=['POST'])
def processjson():
    data = request.get_json()
    return jsonify(data)


x = {
    "name": "bob",
    "array": ['one', 'two']
}

app.run(host='0.0.0.0', debug=True)
