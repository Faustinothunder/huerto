import requests
from datetime import datetime
import json
import csv
import os
from dateutil import parser

# Escribir en el csv
def wcsv(datos, name):
    with open(name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in datos:
            writer.writerow(row)

# Obtener datos previos del csv
def get_existing_data(name):
    existing_data = {}
    if os.path.exists(name):
        with open(name, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                device_eui = row[0]
                existing_data[device_eui] = (float(row[1]), row[2]) 
    return existing_data

# Obtener datos del sensor
def getdataeui(device_eui, medid):
    url = "https://sensecap.seeed.cc/openapi/list_telemetry_data"
    auth = ('93I2S5UCP1ISEF4F', '6552EBDADED14014B18359DB4C3B6D4B3984D0781C2545B6A33727A4BBA1E46E')

    params = {
        'device_eui': device_eui,
        'measurement_id': medid, 
        'limit': 10000,
    }

    r = requests.get(url, params=params, auth=auth)
    print(f"Status Code: {r.status_code}")

    try:
        data = r.json()
        #print(json.dumps(data, indent=2))

        # Extraer los datos de la respuesta
        data_list = data["data"]["list"][1]

        new_data = []
        for sublist in data_list:
            for item in sublist:
                new_data.append((device_eui, float(str(item[0])), item[1]))
        
        existing_data = get_existing_data(f'data{medid}.csv')
        
        last_entry = existing_data.get(device_eui, None)

        # Filtrado de entradas
        if last_entry:
            # Extraer solo las fechas de las entradas y de last_entry
            new_data_dates = [entry[2] for entry in new_data]
            last_entry_date = last_entry[1]

            # Comparar las fechas y filtrar las entradas que sean más recientes que last_entry
            new_data = [entry for entry, date in zip(new_data, new_data_dates) if date > last_entry_date]

        print(new_data)
        # Añadir
        with open(f'data{medid}.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for entry in new_data:
                writer.writerow(entry)
    except json.JSONDecodeError:
        print("No es un JSON")
        print(r.text)

# Llamar a la función para cada dispositivo
getdataeui('2CF7F1C043500730', '4108')
getdataeui('2CF7F1C05230001D', '4108')
getdataeui('2CF7F1C05230009C', '4108')
getdataeui('2CF7F1C0523000A2', '4108')
