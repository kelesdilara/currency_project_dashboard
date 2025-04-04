from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import datetime
import time

# InfluxDB bağlantı bilgileri
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "0xp5VcOdxDo_flh8LiLlvzMsjs398lTU_zT--WgoLxOLfDEJ-50ddwaXe17nSlcPIGI9thogjsF_DgxvQXptXA=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "dovizdb"

def get_exchange_rates():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    if response.status_code == 200:
        return response.json()["rates"]
    else:
        return None

def write_to_influx(data):
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for currency, rate in data.items():
        point = Point("new_exchange_rate").tag("currency", currency).field("rate",float(rate)).time(datetime.datetime.now(datetime.UTC))
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

    client.close()

if __name__ == "__main__":
    while True:
        rates = get_exchange_rates()
        if rates:
            write_to_influx(rates)
            print("Veriler InfluxDB'ye kaydedildi.")
        else:
            print("Döviz kuru verisi alınamadı.")
        time.sleep(0.1)