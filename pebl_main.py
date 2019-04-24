from pyModbusTCP.client import ModbusClient
import time
import json
import csv

CLOSE_MODBUS = False


def csv_json_alarms(system):
    f = open('Alarm_List_' + system + '.csv', 'r')
    f.readline()
    reader = csv.DictReader(f, fieldnames=("alarm", "address", "type"))
    out = json.dumps([row for row in reader])
    return json.loads(out)


class Pebl:
    def __init__(self, ip, system, port=502):
        self.c = ModbusClient(host=ip, port=502, auto_open=True)
        self.c.host(ip)
        self.c.port(port)
        self.c.open()
        self.system = system
        print("opened")

    def run(self):
        return_values = []
        data_points = csv_json_alarms(self.system)
        for data_point in data_points:
            print(data_point)
            if data_point['type'] == 'COIL':
                value = self.c.read_coils(int(data_point['address']))
                print(value)
                name = data_point['alarm']
                return_values.append({'name': name,
                                      'value': value})

        f = open('data.json', 'w')
        f.write(json.dumps(return_values))
        f.close()


def run_thread(address, system):
    pebl = Pebl(address, system)
    while not CLOSE_MODBUS:
        pebl.run()
        print('running')
        time.sleep(5)

if __name__ == '__main__':
    pebl = Pebl('192.168.0.59', '7040')
    pebl.run()


