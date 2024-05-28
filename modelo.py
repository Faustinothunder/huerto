import requests
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import csv
import os
import json
from dateutil import parser

'''
Básicamente, entreno el modelo usando los datos generados teniendo en cuenta el eui del sensor,
intenta predecir si es de dia o de noche sacando informacion del dispositivo. Como las medidas
son diferentes segun el dispositivo, calcula según el dispositivo, y hace un consenso de las 
medidas para determinar si es de dia o de noche, se muestran aun así la fecha/medida y la
predicción según el sensor.
'''

def get_last_measurement(device_eui, medid):
    url = "https://sensecap.seeed.cc/openapi/list_telemetry_data"
    auth = ('93I2S5UCP1ISEF4F', '6552EBDADED14014B18359DB4C3B6D4B3984D0781C2545B6A33727A4BBA1E46E')

    params = {
        'device_eui': device_eui,
        'measurement_id': medid, 
        'limit': 1, 
        'order': 'desc' 
    }

    r = requests.get(url, params=params, auth=auth)
    print(f"Status Code: {r.status_code}")

    try:
        data = r.json()
        print(json.dumps(data, indent=2))

        data_list = data["data"]["list"][1]

        if data_list:
            last_measurement = data_list[0]
            print("Last Measurement:", last_measurement)
            return float(last_measurement[0][0])  # conductividad eléctrica
        else:
            print("No hay datos disponibles para la predicción.")
            return None
    except json.JSONDecodeError:
        print("Response is not in JSON format")
        print(r.text)
        return None


last_measurement = get_last_measurement('2CF7F1C043500730', '4108')
if last_measurement:
    print("Última lectura:", last_measurement)

data = pd.read_csv('data4108.csv', header=None)

X = data.iloc[:, 1:2]  
y = data.iloc[:, 0]  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

if last_measurement:
    nueva_lectura = [[last_measurement]] 
    prediccion = clf.predict(nueva_lectura)
    print("Predicción para la nueva lectura:", "Es de día" if prediccion[0] == 1 else "Es de noche")

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

predicciones = []
dispositivos = ['2CF7F1C043500730', '2CF7F1C05230001D', '2CF7F1C05230009C', '2CF7F1C0523000A2']
for dispositivo in dispositivos:
    last_measurement = get_last_measurement(dispositivo, '4108')
    if last_measurement:
        predicciones.append(last_measurement) 

# Promedio de las predicciones
grado_verdad = sum(predicciones) / len(predicciones)

if grado_verdad >= 0.5:
    print("Es de día (consenso)")
else:
    print("Es de noche (consenso)")
