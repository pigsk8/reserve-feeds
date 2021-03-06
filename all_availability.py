# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta

with open('entry/sistema.json', encoding='utf-8') as file:
    data = json.load(file)

with open('entry/lugares.json', encoding='utf-8') as fileL:
    data_lugar = json.load(fileL)

with open('entry/metas.json', encoding='utf-8') as fileM:
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

print(array_week_dates)
list_lugares = []

f = open('validations/sistema_in.txt', 'r')
f1 = f.readlines()
for x in f1:
    if(x):
        list_lugares.append(int(x))

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
                                    "confirmation_mode": "CONFIRMATION_MODE_ASYNCHRONOUS",
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
                            print('error' + str(lugar['id']))

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
                                    print('error' + str(lugar['id']))

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

                                else:
                                    print('error' + str(lugar['id']))


jsonAvailibilityServ['availability'] = jsonAvailibilityServA
jsonAvailibilityServi.append(jsonAvailibilityServ)

jsonAvailibility['service_availability'] = jsonAvailibilityServi

with open('output/availabilityRecurrence'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonAvailibility, file)
