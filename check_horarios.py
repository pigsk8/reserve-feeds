# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import time
from datetime import datetime, timedelta

with open('entry/sistema.json') as file:
    data = json.load(file)

list_check = []

for lugar in data:
    print(lugar['name']).encode('UTF-8')
    check = 1
    for day in lugar['openingDays']:

        if (check):

            first_hour = second_hour = 0

            if(day['start'] != 0 and day['end'] != 0):
                if(day['start'] is not None and day['end'] is not None):
                    first_hour = 1

            if(day['start2'] != 0 and day['end2'] != 0):
                if(day['start2'] is not None and day['end2'] is not None):
                    second_hour = 1

            if(not first_hour and second_hour):
                check = 0
                list_check.append(lugar['name'])


print(list_check)

with open('listcheck.txt', 'w') as filehandle:
    for single_check in list_check:
        filehandle.write('%s\n' % single_check.encode('utf-8'))

