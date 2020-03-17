# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import date, datetime, timedelta

with open('entry/lugares.json', encoding='utf-8') as file:
    data_lugar = json.load(file)

with open('entry/metas.json', encoding='utf-8') as fileM:
    data_metas = json.load(fileM)

timestamp = int(time.time())

list_empty = []

current_day = date.today()
print(current_day)
current_day_m = current_day.month
current_day_d = current_day.day
c_d = str(current_day.month)+'_'+str(current_day_d)

list_lugares_sys = []
f = open('validations/sistema/sistema_in.txt', 'r')
f1 = f.readlines()
for x in f1:
    if(x):
        list_lugares_sys.append(int(x))

list_lugares = []
for meta in data_metas:
    if meta['meta_key'] == '_sistema_id':
        sistema_id = meta['meta_value']
        number = sistema_id
        try:
            int(number)
        except ValueError:
            pass
        else:
            if int(sistema_id) in list_lugares_sys:
                list_lugares.append(int(meta['post_id']))

# list_lugares = list(dict.fromkeys(list_lugares))
print(len(list_lugares))

id_accept = []

jsonMerchant = {
    "metadata": {
        "generation_timestamp": timestamp,
        "processing_instruction": "PROCESS_AS_COMPLETE",
        "shard_number": 0,
        "total_shards": 1
    }
}
jsonMerchantInfo = []

jsonService = {
    "metadata": {
        "generation_timestamp": timestamp,
        "processing_instruction": "PROCESS_AS_COMPLETE",
        "shard_number": 0,
        "total_shards": 1
    },
}
jsonServiceInfo = []
count = 0

for lugar in data_lugar:

    if int(lugar['ID']) in list_lugares:

        name = lugar['post_title']
        name = name.replace('Restaurante y Bar ', '')
        name = name.replace('Restaurante Bar ', '')
        name = name.replace('Bar Antro ', '')
        name = name.replace('Restaurante ', '')
        name = name.replace('Bar ', '')
        name = name.replace('Antro ', '')

        url = 'https://reservandonos.com/lugar/'+lugar['post_name']+'/'

        sistema_id = 0
        postal_code = "0"

        for meta in data_metas:

            if meta['post_id'] == lugar['ID']:

                if meta['meta_key'] == '_sistema_id':
                    sistema_id = meta['meta_value']

                if meta['meta_key'] == 'geolocation_formatted_address':
                    street_address = meta['meta_value']

                if meta['meta_key'] == 'geolocation_city':
                    locality = meta['meta_value']

                if meta['meta_key'] == 'geolocation_state_short':
                    region = meta['meta_value']

                if meta['meta_key'] == 'geolocation_country_short':
                    country = meta['meta_value']

                if meta['meta_key'] == 'geolocation_postcode':
                    postal_code = meta['meta_value']

        number = sistema_id
        try:
            int(number)
        except ValueError:
            pass
        else:

            if (sistema_id != 0):

                empty = 0
                if (street_address == "" or locality == "" or region == "" or country == "" or postal_code == ""):
                    empty = 1

                if(not empty):

                    count += 1

                    if (count < 41):

                        id_accept.append(int(sistema_id))

                        jsonServiceInfoAdd = [{
                            "url": url
                        }]

                        jsonServiceInfo.append({
                            "merchant_id": "merch"+str(sistema_id),
                            "service_id": str(sistema_id)+"-dining",
                            "name":  "Reservation",
                            "type":  "SERVICE_TYPE_DINING_RESERVATION",
                            "action_link": jsonServiceInfoAdd
                        })

                        jsonMerchantInfoAdd = {
                            "address": {
                                "street_address": street_address,
                                "locality": locality,
                                "region": region,
                                "country": country,
                                "postal_code": postal_code
                            }
                        }

                        jsonMerchantInfo.append({
                            "merchant_id": "merch"+str(sistema_id),
                            "name":  name,
                            "category": "restaurant",
                            "geo": jsonMerchantInfoAdd
                        })

jsonMerchant['merchant'] = jsonMerchantInfo
jsonService['service'] = jsonServiceInfo

id_accept.sort()

with open('listaccept.txt', 'w') as filehandle:
    for accept in id_accept:
        filehandle.write('%s\n' % accept)

with open('output/merchants'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonMerchant, file)

with open('output/services'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonService, file)
