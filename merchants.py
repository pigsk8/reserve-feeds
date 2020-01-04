# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta, date

with open('entry/lugares.json', encoding='utf-8') as file:
    data_lugar = json.load(file)

with open('entry/metas.json', encoding='utf-8') as fileM:
    data_metas = json.load(fileM)

timestamp = int(time.time())

# especificar fecha desde que se hara el recorrido
today = date.today()
c_d = today.strftime("%m_%d")

list_lugares = ['11408', '8676', '1705', '1983', '978', '13365', '13314', '13348', '160', '13319',
                '13417', '11677', '3181', '989', '911', '999', '930', '166', '921', '13291', '5338', '2962', '13459', '12022', '6252', '10042', '13549']

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

    if lugar['ID'] in list_lugares:

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

        if (sistema_id != 0):
            count += 1
            print(str(count) + '. '+str(lugar['ID']))
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

with open('output/merchants'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonMerchant, file)

with open('output/services'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonService, file)
