# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta

with open('entry/lugares.json') as file:
    data_lugar = json.load(file)

with open('entry/metas.json') as fileM:
    data_metas = json.load(fileM)

timestamp = int(time.time())

# especificar fecha desde que se hara el recorrido
fecha = '2019/11/26'
current_day = datetime.strptime(fecha, '%Y/%m/%d')

current_day_m = current_day.month
current_day_d = current_day.day

c_d = str(current_day.month)+'_'+str(current_day_d)

# Lugares a agregar IDs
# Cantina La No. 20 Antara post-1983 id-168
# Restaurante Rosa Negra Tulum post-2546 id-227
# Restaurante Mariachito Insurgentes
# Restaurante Pubbelly Sushi Polanco
# Restaurante Jaso Polanco
# Restaurante Centralito Sur San Ángel
# Restaurante Loveli Lomas De Chapultepec
# Restaurante STK México Polanco
# Restaurante Rosa Negra Cancún
# Restaurante Rosa Negra Polanco

# list_lugares = ['3480', '11317', '6079', '2947', '5198',
#     '6123', '2552', '2540', '2546', '3586', '11421', '1983']

list_lugares = ['1983', '2546']

jsonMerchant = {
    "metadata": {
        "generation_timestamp": timestamp,
        "processing_instruction": "PROCESS_AS_INCREMENTAL",
        "shard_number": 0,
        "total_shards": 1
    }
}
jsonMerchantInfo = []


jsonService = {
    "metadata": {
        "generation_timestamp": timestamp,
        "processing_instruction": "PROCESS_AS_INCREMENTAL",
        "shard_number": 0,
        "total_shards": 1
    },
}
jsonServiceInfo = []

for lugar in data_lugar:
    
    if lugar['ID'] in list_lugares:
        name = lugar['post_title']
        url = 'https://reservandonos.com/lugar/'+lugar['post_name']+'/'

        sistema_id = postal_code = 0

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
