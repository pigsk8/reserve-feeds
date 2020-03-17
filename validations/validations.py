# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

with open('entry/sistema.json', encoding='utf-8') as file:
    data = json.load(file)

with open('entry/lugares.json', encoding='utf-8') as fileL:
    data_lugar = json.load(fileL)

with open('entry/metas.json', encoding='utf-8') as fileM:
    data_metas = json.load(fileM)

print('len sistema '+str(len(data)))
print('len wordpress '+str(len(data_lugar)))

list_lugares = []  # lista de lugares permitidos por id
list_lugares_not = []  # lista d elugares no permitidos

list_lugares_error = []  # lista de errores wordpress merchants

for lugar in data_lugar:

    sistema_id = 0

    lugar_url = 'https://reservandonos.com/lugar/'+lugar['post_name']+'/'
    lugar_name = lugar['post_title']
    lugar_id = lugar['ID']

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
        list_lugares_not.append(int(lugar_id))
        list_lugares_error.append(lugar_name+' - _sistema_id no es numero')
    else:
        if (sistema_id == 0):
            list_lugares_not.append(int(lugar_id))
            list_lugares_error.append(
                lugar_name+' - _sistema_id es cero o no tiene')
        else:
            empty = 0

            if (street_address == ""):
                list_lugares_error.append(
                    lugar_name+' - geolocation_formatted_address')
                empty = 1

            if (locality == ""):
                list_lugares_error.append(lugar_name+' - geolocation_city')
                empty = 1

            if (region == ""):
                list_lugares_error.append(
                    lugar_name+' - geolocation_state_short')
                empty = 1

            if (country == ""):
                list_lugares_error.append(
                    lugar_name+' - geolocation_country_short')
                empty = 1

            if (postal_code == ""):
                list_lugares_error.append(lugar_name+' - geolocation_postcode')
                empty = 1

            if(not empty):
                list_lugares.append(int(sistema_id))
            else:
                list_lugares_not.append(int(lugar_id))

list_lugares = list(dict.fromkeys(list_lugares))
list_lugares_not = list(dict.fromkeys(list_lugares_not))

list_lugares.sort()
list_lugares_not.sort()

Path("validations/wordpress").mkdir(parents=True, exist_ok=True)
# list de aceptados (sistema_id)
with open('validations/wordpress/list_lugares.txt', 'w+') as filehandle:
    for list_sis_id in list_lugares:
        filehandle.write('%s\n' % list_sis_id)

# list de not aceptados (id wordpress)
with open('validations/wordpress/list_lugares_not.txt', 'w+') as filehandle:
    for list_not_id in list_lugares_not:
        filehandle.write('%s\n' % list_not_id)

# list de not aceptados (id wordpress)
with open('validations/wordpress/list_lugares_error.txt', 'w+') as filehandle:
    for list_error in list_lugares_error:
        filehandle.write('%s\n' % list_error.encode('utf-8'))

######################################################################
## Verificacion de horarios de lugares aceptados ##
# tiempo establecido en 7 días para recorrer la semana
fecha = '2019/12/02'
current_day = datetime.strptime(fecha, '%Y/%m/%d')
array_week_dates = [current_day]
for i in range(0, 6):
    array_week_dates.append(current_day + timedelta(days=i+1))

sistema_in = []
sistema_not = []
sistema_error = []  # lista de errores sistema merchants

# lugares nos acpetdos errores de horario
for lugar in data:

    if lugar['id'] in list_lugares:
        lugar_id = lugar['id']
        lugar_name = lugar['name']
        len_hours = len(lugar['openingDays'])

        if len_hours == 0:
            sistema_not.append(int(lugar_id))
            sistema_error.append(str(lugar_name.encode(
                'utf-8')) + ' - no tiene horarios en el sistema')

        elif len_hours > 7:
            sistema_not.append(int(lugar_id))
            sistema_error.append(str(lugar_name.encode(
                'utf-8')) + ' - excede días de la semana')
        else:

            for day in lugar['openingDays']:
                for week_date in array_week_dates:
                    if(week_date.strftime('%A').lower() == day['weekday']):

                        if(day['start'] is not None and day['end'] is not None):
                            if(day['start'] > day['end']):
                                sistema_not.append(int(lugar_id))
                                sistema_error.append(str(lugar_name.encode(
                                    'utf-8')) + ' - es mayor el inicio al final 1')

                        if(day['start2'] is not None and day['end2'] is not None):
                            if(day['start2'] > day['end2']):
                                sistema_not.append(int(lugar_id))
                                sistema_error.append(str(lugar_name.encode(
                                    'utf-8')) + ' - es mayor el inicio al final 2')

                        if (day['start2'] != 0):
                            if(day['start2'] is not None):
                                if (day['end'] >= day['start2']):
                                    sistema_not.append(int(lugar_id))
                                    sistema_error.append(str(lugar_name.encode(
                                        'utf-8')) + ' - el primer fin es mayor o igual al segundo comienzo')

                        if ((day['start'] == 0 and day['end'] == 0) or (day['start'] is None and day['end'] is None)):
                            if (day['start2'] != 0 and day['end2'] != 0):
                                if (day['start2'] is not None and day['end2'] is not None):
                                    sistema_not.append(int(lugar_id))
                                    sistema_error.append(str(lugar_name.encode(
                                        'utf-8')) + ' - Tiene segundo horario pero no tiene primero')

sistema_not = list(dict.fromkeys(sistema_not))

# lugares aceptados
for lugar in data:
    if int(lugar['id']) in list_lugares:
        if int(lugar['id']) not in sistema_not:
            sistema_in.append(lugar['id'])

sistema_in = list(dict.fromkeys(sistema_in))

sistema_in.sort()
sistema_not.sort()

Path("validations/sistema").mkdir(parents=True, exist_ok=True)

# lista de aceptados finales (sistema_id)
with open('validations/sistema/sistema_in.txt', 'w') as filehandle:
    for list_sis_id in sistema_in:
        filehandle.write('%s\n' % list_sis_id)

# list de not aceptados sistema (sistema_id)
with open('validations/sistema/sistema_not.txt', 'w') as filehandle:
    for list_not_id in sistema_not:
        filehandle.write('%s\n' % list_not_id)

# list de no aceptados (error sistema horarios)
with open('validations/sistema/sistema_error.txt', 'w') as filehandle:
    for list_error in sistema_error:
        filehandle.write('%s\n' % list_error)
