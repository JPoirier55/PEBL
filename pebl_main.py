from pyModbusTCP.client import ModbusClient
import time
import json
import csv
import xlsxwriter

CLOSE_MODBUS = False

def csv_json_addresses():
    f = open('Address List.csv', 'r')
    f.readline()
    reader = csv.DictReader(f, fieldnames=("name", "address", "system"))
    out = json.dumps([row for row in reader])
    return json.loads(out)

def csv_json_alarms(system):
    f = open('Alarm_List_' + system + '.csv', 'r')
    f.readline()
    reader = csv.DictReader(f, fieldnames=("alarm", "address", "type", "trigger"))
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

    def run_manual(self):
        return_values = []
        data_points = csv_json_alarms(self.system)
        for data_point in data_points:
            print(data_point)
            if data_point['type'] == 'COIL':
                value = self.c.read_coils(int(data_point['address']))
                name = data_point['alarm']
                if data_point['trigger'] == 'NC':
                    if not value[0]:
                        return_values.append({'name': name,
                                              'value': 'OK'})
                    else:
                        return_values.append({'name': name,
                                              'value': 'ALARM'})
                elif data_point['trigger'] == 'NO':
                    if value[0]:
                        return_values.append({'name': name,
                                              'value': 'ALARM'})
                    else:
                        return_values.append({'name': name,
                                              'value': 'OK'})
        return return_values


def run_thread(address, system):
    pebl = Pebl(address, system)
    while not CLOSE_MODBUS:
        pebl.run()
        print('running')
        time.sleep(5)


def run_manual():
    outputs = []
    for system in csv_json_addresses():

        pebl = Pebl('192.168.0.59', '7040')
        outputs.append({'name': system['name'] + '-' + system['system'],
                        'system': system['system'],
                        'ip': system['address'],
                        'alarms': pebl.run_manual()})
        pebl.c.close()
    print(outputs)
    clean_outputs(outputs)


def clean_outputs(outputs):
    workbook = xlsxwriter.Workbook('Report.xlsx')
    red_cell = workbook.add_format({'bold': True, 'font_color': 'red', 'bg_color': '#f4c8c8'})
    green_cell = workbook.add_format({'bold': True, 'font_color': 'green', 'bg_color': '#dbf4c8'})
    second_header_cell = workbook.add_format({'bold': True, 'font_size': 15, 'bg_color': '#e2e2e2'})
    worksheet = workbook.add_worksheet()
    for i in range(5):
        worksheet.set_column(i, 0, 25)
    index = 1
    for dict_obj in outputs:
        worksheet.write_row('A'+str(index), (dict_obj['name'], dict_obj['ip']), second_header_cell)
        index += 1
        for alarm in dict_obj['alarms']:
            print(alarm)
            if alarm['value'] == 'ALARM':
                worksheet.write_row('A'+str(index), (str(alarm['name']), str(alarm['value'])), red_cell)
            else:
                worksheet.write_row('A' + str(index), (str(alarm['name']), str(alarm['value'])), green_cell)
            index += 1
    workbook.close()
    # f = open('Report.csv', 'w')
    # csv_writer = csv.writer(f, delimiter=',')
    # csv_writer.writerow(('IP', 'SYSTEM', 'ALARMS', 'VALUE'))
    # for dict_obj in outputs:
    #     csv_writer.writerow((dict_obj['ip'], dict_obj['system']))
    #     for alarm in dict_obj['alarms']:
    #         print(alarm)
    #         csv_writer.writerow(('', '', alarm['name'], alarm['value']))

if __name__ == '__main__':
    # clean_outputs('sdf')

    run_manual()


