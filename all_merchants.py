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

list_empty = []

# especificar fecha desde que se hara el recorrido
fecha = '2019/12/03'
current_day = datetime.strptime(fecha, '%Y/%m/%d')

current_day_m = current_day.month
current_day_d = current_day.day

c_d = str(current_day.month)+'_'+str(current_day_d)

# list_lugares = ['11408','8676','2047','6124']

list_not_lugares = [315, 43, 314, 339, 194, 236, 212, 417, 268, 16, 403, 1008, 274, 316, 234, 1004, 273, 252, 260, 245, 592, 487, 568, 545, 55, 584, 540, 450, 443, 542, 558, 500,
                    459, 550, 557, 644, 575, 525, 617, 47, 852, 84, 668, 872, 655, 835, 723, 810, 805, 676, 709, 809, 654, 799, 646, 824, 823, 876, 660, 949, 955, 946, 994, 9, 996, 942, 972, 998, 933]

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
id_accept = []
dict_accept = {}

for lugar in data_lugar:

    # if lugar['ID'] in list_lugares:
    name = lugar['post_title'].encode("utf-8")
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
        list_empty.append(url+' - _sistema_id no es numero')
    else:
        if (sistema_id == 0):
            list_empty.append(url+' - _sistema_id es cero')

        if (sistema_id != 0):

            empty = 0

            if (street_address == ""):
                list_empty.append(url+' - geolocation_formatted_address')
                empty = 1

            if (locality == ""):
                list_empty.append(url+' - geolocation_city')
                empty = 1

            if (region == ""):
                list_empty.append(url+' - geolocation_state_short')
                empty = 1

            if (country == ""):
                list_empty.append(url+' - geolocation_country_short')
                empty = 1

            if (postal_code == ""):
                list_empty.append(url+' -geolocation_postcode')
                empty = 1

            if(not empty):

                count += 1

                if str(sistema_id) not in str(list_not_lugares):

                    if (count < 101):

                        id_accept.append(sistema_id)
                        
                        dict_accept[sistema_id] = lugar['ID']
                        
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

# with open('listfile.txt', 'w') as filehandle:
#     for empty in list_empty:
#         filehandle.write('%s\n' % empty)

for key in sorted(dict_accept.keys()) :
    print(key , " :: " , dict_accept[key])

with open('listacept.txt', 'w') as filehandle:
    for accept in id_accept:
        filehandle.write('%s\n' % accept)

with open('output/merchants'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonMerchant, file)

with open('output/services'+str(c_d)+'.json', 'w') as file:
    json.dump(jsonService, file)
