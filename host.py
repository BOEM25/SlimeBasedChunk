from os import listdir

from flask import Flask, jsonify, request
from ilog.console import log
import json

app = Flask(__name__)

current = 0
step_size = 200000000
maxX = 281474976710656
fhinished = 0

x = [1, 3, 4, 5, 1, 3, 2, 9, 10]
z = [2, 2, 0, 5, 4, 6, 6, 5, 7]

with open('data/ids.json', 'r') as f:
    ids = json.load(f)
    highd = max(ids['ids'])
    log(highd)
    current = highd*step_size
    log(current)
    f.close()

with open('data/sets.json', 'r') as f:
    sets = json.load(f)
    for i in sets:
        state = sets[i]
        if not state:
            log(state)
    f.close()


@app.route("/")
def home():
    return f"API For the slimechunk Project {request.remote_addr}", 200


@app.route("/heartbeat")
def heartbeat():
    return "200", 200


x = {
    "seeds": [123123, 23452345],
    "set": 1,

}


@app.route("/seeds", methods=['POST'])
def working_seeds():
    data2 = request.data.decode()
    data = json.loads(data2)
    log(data, request.remote_addr)
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
    data2 = request.data.decode()
    data = json.loads(data2)
    log(data, request.remote_addr)
    if data['state'] == True:
        state = True
    else:
        state = False

    with open('data/sets.json', 'r') as f:
        sets = json.load(f)
        f.close()

    sets[data['set']] = state

    with open('data/sets.json', 'w') as f:
        json.dump(sets, f, indent=4)
        f.close()

    return "coolio", 200


@app.route("/id", methods=['GET'])
def get_id():
    with open('data/ids.json', 'r') as f:
        ids = json.load(f)
        f.close()


@app.route("/state", methods=['GET'])
def give_state():
    global maxX, current, step_size
    global fhinished
    global x, z

    temp = False



    with open('data/ids.json', 'r') as f:
        ids = json.load(f)
        f.close()

    if temp == False:
        id = list(ids['ids'])

        highest = max(id)
        id.append(highest + 1)

    seedRange = current + step_size

    if seedRange >= maxX:

        if fhinished > 0:
            log("Complete", request.remote_addr)
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
    data2 = request.data.decode()
    f = json.loads(data2)
    log(f, request.remote_addr)
    return jsonify(f)


x = {
    "name": "bob",
    "array": ['one', 'two']
}

# First GET /state is called to get data, then the node does its calculations, then POST /done and  POST /seeds(with the found seeds and id) then starts again at POST /state

app.run(host='0.0.0.0', debug=True)
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_cached_json', '_get_data_for_json', '_get_file_stream', '_get_stream_for_parsing', '_load_form_data', '_parse_content_type', 'accept_charsets', 'accept_encodings', 'accept_languages', 'accept_mimetypes', 'access_control_request_headers', 'access_control_request_method', 'access_route', 'application', 'args', 'authorization', 'base_url', 'blueprint', 'cache_control', 'charset', 'close', 'content_encoding', 'content_length', 'content_md5', 'content_type', 'cookies', 'data', 'date', 'dict_storage_class', 'disable_data_descriptor', 'encoding_errors', 'endpoint', 'environ', 'files', 'form', 'form_data_parser_class', 'from_values', 'full_path', 'get_data', 'get_json', 'headers', 'host', 'host_url', 'if_match', 'if_modified_since', 'if_none_match', 'if_range', 'if_unmodified_since', 'input_stream', 'is_json', 'is_multiprocess', 'is_multithread', 'is_run_once', 'is_secure', 'json', 'json_module', 'list_storage_class', 'make_form_data_parser', 'max_content_length', 'max_form_memory_size', 'max_forwards', 'method', 'mimetype', 'mimetype_params', 'on_json_loading_failed', 'origin', 'parameter_storage_class', 'path', 'pragma', 'query_string', 'range', 'referrer', 'remote_addr', 'remote_user', 'routing_exception', 'scheme', 'script_root', 'shallow', 'stream', 'trusted_hosts', 'url', 'url_charset', 'url_root', 'url_rule', 'user_agent', 'values', 'view_args', 'want_form_data_parsed']
