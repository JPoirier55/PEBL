from flask import Flask
from flask import request
from flask import render_template
import pebl_main
import threading
import json
import csv
app = Flask(__name__)


def csv_json_addresses():
    f = open('Address List.csv', 'r')
    f.readline()
    reader = csv.DictReader(f, fieldnames=("name", "address", "system"))
    out = json.dumps([row for row in reader])
    return json.loads(out)

@app.route("/")
def monitor():
    return render_template('main.html')

@app.route("/api/data")
def pebl_data():
    f = open('data.json', 'r')
    json_obj = json.loads(f.read())
    return json.dumps(json_obj)


@app.route("/api/start")
def pebl_starter():
    start = request.args.get('start')
    if start == 'true':
        pebl_main.CLOSE_MODBUS = False
        for system in csv_json_addresses():
            ip = system['address']
            system_type = system['system']
            t = threading.Thread(target=pebl_main.run_thread, args=(ip, system_type))
            t.start()
        return 'Connected'
    else:
        pebl_main.CLOSE_MODBUS = True
        return 'Disconnected'

if __name__ == "__main__":
    app.run(debug=True)