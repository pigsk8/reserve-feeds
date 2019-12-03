# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta

with open('entry/sistema.json') as file:
    data = json.load(file)

with open('entry/lugares.json') as fileL:
    data_lugar = json.load(fileL)

with open('entry/metas.json') as fileM:
    data_metas = json.load(fileM)

timestamp = int(time.time())

# especificar fecha desde que se hara el recorrido
fecha = '2019/12/02'
current_day = datetime.strptime(fecha, '%Y/%m/%d')

current_day_m = current_day.month
current_day_d = current_day.day

c_d = str(current_day.month)+'_'+str(current_day_d)

array_week_dates = [current_day]

# definir fecha a 30 dias
for i in range(0, 8):
    array_week_dates.append(current_day + timedelta(days=i+1))

list_wrong = {}
list_lugares = []
# list_lugares = [248, 77, 985, 986, 987, 988, 989, 990, 992, 993, 994, 995, 996, 997, 998, 1008, 1000, 1001, 47, 55, 57, 71, 81,
#                 82, 84, 87, 88, 89, 92, 93, 94, 95, 96, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 121, 150, 151, 153, 157]

# list_lugares.sort()

# print(list_lugares)

# exit()

for lugar in data_lugar:

    sistema_id = 0

    for meta in data_metas:

        if meta['post_id'] == lugar['ID']:

            if meta['meta_key'] == '_sistema_id':
                sistema_id = meta['meta_value']

    no = 0
    number = sistema_id
    try:
        int(number)
    except ValueError:
        no = 0
    else:
        if (sistema_id != 0):
            list_lugares.append(int(sistema_id))


jsonAvailibility = {
    "metadata": {
        "processing_instruction": "PROCESS_AS_COMPLETE",
        "shard_number": 0,
        "total_shards": 1,
        "generation_timestamp": timestamp
    }
}

jsonAvailibilityServ = {}
jsonAvailibilityServi = []
jsonAvailibilityServA = []

for lugar in data:
    if lugar['id'] in list_lugares:

        for day in lugar['openingDays']:

            for week_date in array_week_dates:
                if(week_date.strftime('%A').lower() == day['weekday']):

                    double_check = 0

                    if (day['start'] is not None and day['end'] is not None and day['start2'] is not None and day['end2'] is not None):
                        double_check = 1

                    if(double_check and (day['start'] != 0 and day['end'] != 0 and day['start2'] != 0 and day['end2'] != 0)):

                        # con recurrencia y excepciones
                        if(day['end'] > day['start'] and day['end2'] > day['start2'] and day['start2'] > day['end']):

                            dt_start = week_date + \
                                timedelta(seconds=day['start']*60)
                            timestamp_start = (
                                dt_start - datetime(1970, 1, 1)).total_seconds()

                            dt_end = week_date + \
                                timedelta(seconds=(day['end'])*60)
                            timestamp_end = (
                                dt_end - datetime(1970, 1, 1)).total_seconds()

                            dt_start2 = week_date + \
                                timedelta(seconds=day['start2']*60)
                            timestamp_start2 = (
                                dt_start2 - datetime(1970, 1, 1)).total_seconds()

                            dt_end2 = week_date + \
                                timedelta(seconds=(day['end2']-30)*60)
                            timestamp_end2 = (
                                dt_end2 - datetime(1970, 1, 1)).total_seconds()

                            for party_size in range(1, 11):
                                jsonAvailibilityServA.append({
                                    "duration_sec": 1800,
                                    "start_sec": int(timestamp_start),
                                    "merchant_id": "merch"+str(lugar['id']),
                                    "service_id": str(lugar['id'])+"-dining",
                                    "spots_open": 10,
                                    "spots_total": 10,
                                    "ConfirmationMode": "CONFIRMATION_MODE_ASYNCHRONOUS",
                                    "resources": {
                                        "party_size": party_size
                                    },
                                    "recurrence": {
                                        "repeat_until_sec": int(timestamp_end2),
                                        "repeat_every_sec": 1800
                                    },
                                    "schedule_exception": [
                                        {
                                            "time_range": {
                                                "begin_sec": int(timestamp_end),
                                                "end_sec": int(timestamp_start2)
                                            }
                                        }
                                    ]
                                })

                        else:
                            list_wrong[lugar['name'].encode('UTF-8')] = day['weekday']

                    else:

                        #######################################
                        # RECURRENCIA
                        if(day['start'] != 0 and day['end'] != 0):

                            if(day['start'] is not None and day['end'] is not None):

                                if(day['end'] > day['start']):

                                    dt_start = week_date + \
                                        timedelta(seconds=day['start']*60)
                                    timestamp_start = (
                                        dt_start - datetime(1970, 1, 1)).total_seconds()

                                    dt_end = week_date + \
                                        timedelta(seconds=(day['end']-30)*60)
                                    timestamp_end = (
                                        dt_end - datetime(1970, 1, 1)).total_seconds()

                                    for party_size in range(1, 11):
                                        jsonAvailibilityServA.append({
                                            "duration_sec": 1800,
                                            "start_sec": int(timestamp_start),
                                            "merchant_id": "merch"+str(lugar['id']),
                                            "service_id": str(lugar['id'])+"-dining",
                                            "spots_open": 10,
                                            "spots_total": 10,
                                            "resources": {
                                                "party_size": party_size
                                            },
                                            "recurrence": {
                                                "repeat_until_sec": int(timestamp_end),
                                                "repeat_every_sec": 1800
                                            },
                                            "confirmation_mode": "CONFIRMATION_MODE_ASYNCHRONOUS"
                                        })

                                else:
                                    list_wrong[lugar['name'].encode('UTF-8')] = day['weekday']

                        if(day['start2'] != 0 and day['end2'] != 0):

                            if(day['start2'] is not None and day['end2'] is not None):

                                if(day['end2'] > day['start2']):

                                    dt_start = week_date + \
                                        timedelta(seconds=day['start2']*60)
                                    timestamp_start = (
                                        dt_start - datetime(1970, 1, 1)).total_seconds()

                                    dt_end = week_date + \
                                        timedelta(seconds=(day['end2']-30)*60)
                                    timestamp_end = (
                                        dt_end - datetime(1970, 1, 1)).total_seconds()

                                    for party_size in range(1, 11):
                                        jsonAvailibilityServA.append({
                                            "duration_sec": 1800,
                                            "start_sec": int(timestamp_start),
                                            "merchant_id": "merch"+str(lugar['id']),
                                            "service_id": str(lugar['id'])+"-dining",
                                            "spots_open": 10,
                                            "spots_total": 10,
                                            "resources": {
                                                "party_size": party_size
                                            },
                                            "recurrence": {
                                                "repeat_until_sec": int(timestamp_end),
                                                "repeat_every_sec": 1800
                                            },
                                            "confirmation_mode": "CONFIRMATION_MODE_ASYNCHRONOUS"
                                        })

                                list_wrong[lugar['name'].encode('UTF-8')] = day['weekday']


jsonAvailibilityServ['availability'] = jsonAvailibilityServA
jsonAvailibilityServi.append(jsonAvailibilityServ)

jsonAvailibility['service_availability'] = jsonAvailibilityServi

with open('list_wrong.json', 'w') as filew:
    filew.write(json.dumps(list_wrong))

with open('output/availabilityRecurrence'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonAvailibility, file)
