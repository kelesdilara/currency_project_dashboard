from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
import datetime
from datetime import timezone
import time
import csv

# InfluxDB bağlantı bilgileri
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "0xp5VcOdxDo_flh8LiLlvzMsjs398lTU_zT--WgoLxOLfDEJ-50ddwaXe17nSlcPIGI9thogjsF_DgxvQXptXA=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "dovizdb"

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

csv_file_path = "tr.csv"

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    counter = 0
    for row in csv_reader:
        date_str = row['date']
        value = float(row['value'])

        date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)

        point = Point("historical_tr") \
            .tag("currency", "TRY") \
            .field("rate", value) \
            .time(date_time)

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        counter +=1
        print(counter)


client.close()

print("Data successfully written to InfluxDB!")