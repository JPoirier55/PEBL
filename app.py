from flask import Flask
from flask import request
from flask import render_template
import main_runner
import threading
import json
app = Flask(__name__)

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
        main_runner.CLOSE_MODBUS = False
        t = threading.Thread(target=main_runner.run_thread)
        t.start()
        return 'Connected'
    else:
        main_runner.CLOSE_MODBUS = True
        return 'Disconnected'

if __name__ == "__main__":
    app.run()