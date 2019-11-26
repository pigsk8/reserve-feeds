# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta

with open('entry/sistema880.json') as file:
    data = json.load(file)

timestamp = int(time.time())

#especificar fecha desde que se hara el recorrido
fecha = '2019/11/26'
current_day = datetime.strptime(fecha, '%Y/%m/%d')
current_day_d = current_day.day

array_week_dates = [current_day]

#definir fecha a 30 dias
for i in range(0, 30):
    array_week_dates.append(current_day + timedelta(days=i+1))
    
list_lugares = [880]

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
                    
                    if(day['start'] != 0 and day['end'] != 0):

                        for minutes in range(day['start'],day['end'],(1800/60)):
                            dt = week_date + timedelta(seconds=minutes*60)
                            timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
                            for party_size in range(1,11):
                                jsonAvailibilityServA.append({
                                    "duration_sec": 1800, 
                                    "start_sec": int(timestamp),
                                    "merchant_id": "merch"+str(lugar['id']),
                                    "service_id": str(lugar['id'])+"-dining",
                                    "spots_open": 10,
                                    "spots_total": 10,
                                    "resources": {
                                        "party_size": party_size
                                    },
                                    "confirmation_mode": "CONFIRMATION_MODE_ASYNCHRONOUS" 
                                })


                    if(day['start2'] != 0 and day['end2'] != 0):

                        for minutes in range(day['start2'],day['end2'],(1800/60)):
                            dt = week_date + timedelta(seconds=minutes*60)
                            timestamp = (dt - datetime(1970, 1, 1)).total_seconds()
                            for party_size in range(1,11):
                                jsonAvailibilityServA.append({
                                    "duration_sec": 1800, 
                                    "start_sec": int(timestamp),
                                    "merchant_id": "merch"+str(lugar['id']),
                                    "service_id": str(lugar['id'])+"-dining",
                                    "spots_open": 10,
                                    "spots_total": 10,
                                    "resources": {
                                        "party_size": party_size
                                    },
                                    "confirmation_mode": "CONFIRMATION_MODE_ASYNCHRONOUS"
                                })

jsonAvailibilityServ['availability'] = jsonAvailibilityServA
jsonAvailibilityServi.append(jsonAvailibilityServ)

jsonAvailibility['service_availability'] = jsonAvailibilityServi

with open('output/availibility880.json', 'w') as file:
    json.dump(jsonAvailibility, file)
