# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta, date
import pytz
import sys
from random import randint
from pathlib import Path

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def is_date(date_text):
    try:
        datetime.strptime(date_text, '%Y/%m/%d')
    except ValueError:
        return False
    else:
        return True


# especificar fecha desde que se hara el recorrido
if len(sys.argv) > 1:
    new_date = sys.argv[1]
    if (is_date(new_date)):
        current_day = datetime.strptime(new_date, '%Y/%m/%d')
    else:
        current_day = date.today()
else:
    current_day = date.today()

current_day_m = current_day.month
current_day_d = current_day.day
c_d = str(current_day.month)+'_'+str(current_day_d)

utc_timezone = pytz.timezone("UTC")
naive_utc = datetime.strptime("1970-1-1", "%Y-%m-%d")
utc_date = utc_timezone.localize(naive_utc, is_dst=None)

with open('entry/sistema.json', encoding='utf-8') as file:
    data = json.load(file)

timestamp_init = int(time.time())

array_week_dates = [datetime.combine(
    current_day + timedelta(days=0), datetime.min.time())]

# definir fecha a X dias
for i in range(0, 8):
    array_week_dates.append(datetime.combine(
        current_day + timedelta(days=i+1), datetime.min.time()))

list_lugares = []

f = open('listaccept.txt', 'r')
f1 = f.readlines()
for x in f1:
    if(x):
        list_lugares.append(int(x))

shard_number = 0
total_shard = len(list_lugares)
nonce = int(random_with_N_digits(10))

#if 2 mean 1 persona
max_personas_mesa = 3
#tiempo_mesa in sec
tiempo_mesa = 900
tiempo_menos_final = int(tiempo_mesa/60)

for lugar in data:

    if lugar['id'] in list_lugares:

        jsonAvailibility = {
            "metadata": {
                "processing_instruction": "PROCESS_AS_COMPLETE",
                "shard_number": shard_number,
                "total_shards": total_shard,
                "nonce": int(nonce),
                "generation_timestamp": int(timestamp_init)
            }
        }

        shard_number += 1

        jsonAvailibilityServ = {}
        jsonAvailibilityServi = []
        jsonAvailibilityServA = []

        local_timezone = pytz.timezone(lugar['timezone'])

        for week_date in array_week_dates:
            
            for day in lugar['openingDays']:

                # if(week_date.strftime('%A').lower() == day['weekday'] and (day['weekday'] == 'wednesday' or day['weekday'] == 'thursday' or day['weekday'] == 'friday')):
                if(week_date.strftime('%A').lower() == day['weekday']):

                    if(day['start'] != 0 and day['end'] != 0):
                        if(day['start'] is not None and day['end'] is not None):

                            for minutes in range(day['start'], day['end'], (tiempo_menos_final)):
                                # dt = week_date + timedelta(seconds=minutes*60)
                                # timestamp = (dt - datetime(1970, 1, 1)).total_seconds()

                                dt = week_date + timedelta(seconds=minutes*60)
                                local_dt = local_timezone.localize(
                                    dt, is_dst=None)
                                timestamp = (
                                    local_dt - utc_date).total_seconds()

                                # if(day['weekday'] == 'wednesday'):
                                #     print(day['weekday'])
                                #     print(dt)
                                #     print(local_dt)
                                #     print(timestamp)
                                #     print()

                                for party_size in range(1, max_personas_mesa):
                                    jsonAvailibilityServA.append({
                                        "duration_sec": tiempo_mesa,
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
                        if(day['start2'] is not None and day['end2'] is not None):

                            for minutes in range(day['start2'], day['end2'], (tiempo_menos_final)):
                                # dt = week_date + timedelta(seconds=minutes*60)
                                # timestamp = (dt - datetime(1970, 1, 1)).total_seconds()

                                dt = week_date + timedelta(seconds=minutes*60)
                                local_dt = local_timezone.localize(
                                    dt, is_dst=None)
                                timestamp = (
                                    local_dt - utc_date).total_seconds()

                                # if(day['weekday'] == 'wednesday'):
                                #     print(day['weekday'])
                                #     print(dt)
                                #     print(local_dt)
                                #     print(timestamp)
                                #     print()

                                for party_size in range(1, max_personas_mesa):
                                    jsonAvailibilityServA.append({
                                        "duration_sec": tiempo_mesa,
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

        Path('output/availibility'+c_d).mkdir(parents=True, exist_ok=True)
        with open('output/availibility'+c_d+'/availibility_'+c_d+'_'+str(lugar['id'])+'_'+str(shard_number)+'of'+str(total_shard)+'.json', 'w') as file:
            json.dump(jsonAvailibility, file)
