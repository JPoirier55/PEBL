
from pyModbusTCP.client import ModbusClient
import data
import time
import json

CLOSE_MODBUS = False


class Pebl:
    def __init__(self, ip, port=502):
        self.c = ModbusClient(host=ip, port=502, auto_open=True)
        self.c.host(ip)
        self.c.port(port)
        self.c.open()
        print("opened")

    def run(self):
        address_obj = data.addressing_7040['data_points']
        return_values = []
        for data_point in address_obj:
            if data_point['type'] == 'COIL':
                value = self.c.read_coils(data_point['address'])
                name = data_point['name']
                return_values.append({'name': name,
                                      'value': value})

        f = open('data.json', 'w')
        f.write(json.dumps(return_values))
        f.close()


def run_thread():
    pebl = Pebl('192.168.0.59')
    while not CLOSE_MODBUS:
        pebl.run()
        print('running')
        time.sleep(5)




