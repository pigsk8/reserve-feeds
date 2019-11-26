# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta

#https://reservandonos.com/wp-json/webinfinitech/v1/get-data-places
with open('entry/lugares.json') as file:
	data_lugar = json.load(file)

#https://reservandonos.com/wp-json/webinfinitech/v1/get-data-places-metas
with open('entry/metas.json') as fileM:
	data_metas = json.load(fileM)

timestamp = int(time.time())

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

name = 'Restaurante Leo'
url = 'https://reservandonos.com/lugar/restaurante-leo/'
sistema_id = 880
street_address = 'Avenida Ejército Nacional 843, Granada, 11520 Miguel Hidalgo, CDMX, México'
locality = 'Miguel Hidalgo'
region = 'CDMX'
country = 'MX'
postal_code = '11520'

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

with open('output/merchant880.json', 'w') as file:
    json.dump(jsonMerchant, file)

with open('output/service880.json', 'w') as file:
    json.dump(jsonService, file)
