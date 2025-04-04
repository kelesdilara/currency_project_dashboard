from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime
from datetime import timezone
import csv
import os
from dotenv import load_dotenv
load_dotenv()


INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")


client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

csv_file_path = "values2.csv"

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    counter = 0
    for row in csv_reader:
        date_str = row['date']
        value = float(row['value'])

        date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)

        point = Point("historical_euro") \
            .tag("currency", "EUR") \
            .field("rate", value) \
            .time(date_time)

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        counter +=1
        print(counter)


client.close()

print("Data successfully written to InfluxDB!")