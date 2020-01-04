# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta, date
import pytz
import sys


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

# local = pytz.timezone ("America/Caracas")
# naive = datetime.strptime ("2019-12-26 15:37:12", "%Y-%m-%d %H:%M:%S")
# local_dt = local.localize(naive, is_dst=None)
utc_timezone = pytz.timezone("UTC")
naive_utc = datetime.strptime("1970-1-1", "%Y-%m-%d")
utc_date = utc_timezone.localize(naive_utc, is_dst=None)
# timestamp_start = (local_dt - utc_date).total_seconds()

with open('entry/sistema.json', encoding='utf-8') as file:
    data = json.load(file)

timestamp = int(time.time())

array_week_dates = [datetime.combine(current_day + timedelta(days=0), datetime.min.time())]
# definir fecha a X dias
for i in range(0, 8):
    array_week_dates.append(datetime.combine(current_day + timedelta(days=i+1), datetime.min.time()))

list_lugares = []

f = open('listaccept.txt', 'r')
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
count = 0

max_personas_mesa = 5
tiempo_mesa = 900
tiempo_menos_final = int(tiempo_mesa/60)

for lugar in data:

    if lugar['id'] in list_lugares:
        count += 1
        local_timezone = pytz.timezone(lugar['timezone'])

        print(str(count)+'. '+str(lugar['id'])+' - '+lugar['timezone'])
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
                            local_dt_start = local_timezone.localize(
                                dt_start, is_dst=None)
                            timestamp_start = (
                                local_dt_start - utc_date).total_seconds()

                            dt_end = week_date + \
                                timedelta(seconds=(day['end'])*60)
                            local_dt_end = local_timezone.localize(
                                dt_end, is_dst=None)
                            timestamp_end = (
                                local_dt_end - utc_date).total_seconds()

                            dt_start2 = week_date + \
                                timedelta(seconds=day['start2']*60)
                            local_dt_start2 = local_timezone.localize(
                                dt_start2, is_dst=None)
                            timestamp_start2 = (
                                local_dt_start2 - utc_date).total_seconds()

                            dt_end2 = week_date + \
                                timedelta(seconds=(day['end2']-tiempo_menos_final)*60)
                            local_dt_end2 = local_timezone.localize(
                                dt_end2, is_dst=None)
                            timestamp_end2 = (
                                local_dt_end2 - utc_date).total_seconds()

                            for party_size in range(1, max_personas_mesa):
                                jsonAvailibilityServA.append({
                                    "duration_sec": tiempo_mesa,
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
                                        "repeat_every_sec": tiempo_mesa
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

                        #######################################
                        # RECURRENCIA
                        if(day['start'] != 0 and day['end'] != 0):

                            if(day['start'] is not None and day['end'] is not None):

                                if(day['end'] > day['start']):
                                    dt_start = (week_date + timedelta(seconds=day['start']*60))
                                    local_dt_start = local_timezone.localize(
                                        dt_start, is_dst=None)
                                    timestamp_start = (
                                        local_dt_start - utc_date).total_seconds()

                                    dt_end = week_date + \
                                        timedelta(seconds=(day['end']-tiempo_menos_final)*60)
                                    local_dt_end = local_timezone.localize(
                                        dt_end, is_dst=None)
                                    timestamp_end = (
                                        local_dt_end - utc_date).total_seconds()

                                    if(lugar['id'] == 986):
                                        print(dt_start)
                                        print(local_dt_start)
                                        print(timestamp_start)
                                        print(dt_end)
                                        print(local_dt_end)
                                        print(timestamp_end)
                                        print()

                                    for party_size in range(1, max_personas_mesa):
                                        jsonAvailibilityServA.append({
                                            "duration_sec": tiempo_mesa,
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
                                                "repeat_every_sec": tiempo_mesa
                                            },
                                            "confirmation_mode": "CONFIRMATION_MODE_ASYNCHRONOUS"
                                        })

                        if(day['start2'] != 0 and day['end2'] != 0):

                            if(day['start2'] is not None and day['end2'] is not None):

                                if(day['end2'] > day['start2']):
                                    dt_start = week_date + \
                                        timedelta(seconds=day['start2']*60)
                                    local_dt_start = local_timezone.localize(
                                        dt_start, is_dst=None)
                                    timestamp_start = (
                                        local_dt_start - utc_date).total_seconds()

                                    dt_end = week_date + \
                                        timedelta(seconds=(day['end2']-tiempo_menos_final)*60)
                                    local_dt_end = local_timezone.localize(
                                        dt_end, is_dst=None)
                                    timestamp_end = (
                                        local_dt_end - utc_date).total_seconds()

                                    for party_size in range(1, max_personas_mesa):
                                        jsonAvailibilityServA.append({
                                            "duration_sec": tiempo_mesa,
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
                                                "repeat_every_sec": tiempo_mesa
                                            },
                                            "confirmation_mode": "CONFIRMATION_MODE_ASYNCHRONOUS"
                                        })


jsonAvailibilityServ['availability'] = jsonAvailibilityServA
jsonAvailibilityServi.append(jsonAvailibilityServ)

jsonAvailibility['service_availability'] = jsonAvailibilityServi

with open('output/availabilityRecurrence'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonAvailibility, file)
