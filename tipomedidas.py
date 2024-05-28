import requests

def get_sensor_measure_list():
    url = "https://sensecap-statics.seeed.cn/refer/def/sensor.json"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
        return None

sensor_measure_list = get_sensor_measure_list()
if sensor_measure_list:
    # Imprimir la lista de sensores y mediciones
    print("Sensor Types:")
    for sensor_id, sensor_name in sensor_measure_list['en']['sensorType'].items():
        print(f"Sensor ID: {sensor_id}, Name: {sensor_name}")

    print("\nMeasurements:")
    for measure_id, measure_info in sensor_measure_list['en']['measurementId'].items():
        print(f"Measurement ID: {measure_id}, Name: {measure_info[0]}, Unit: {measure_info[1]}")
else:
    print("Failed to retrieve sensor measure list.")
