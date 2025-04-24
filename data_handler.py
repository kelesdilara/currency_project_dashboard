import sys
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime
from datetime import timezone
import csv
import os
from dotenv import load_dotenv
from logger import setup_logger
load_dotenv()

logger = setup_logger(__name__)

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)




if len(sys.argv) != 2:

    logger.error("Usage: no argument (currency name) provided")
    sys.exit(1)

# Read the file name from the command line argument
filename = sys.argv[1]
csv_file_path = f'{filename}.csv'

try:
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        counter = 0
        for row in csv_reader:
            date_str = row['date']
            value = float(row['value'])
            date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)

            point = Point(f"eur_exchange_{filename}") \
                .tag("currency", f"{filename}") \
                .field("rate", value) \
                .time(date_time)

            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            counter += 1

    client.close()


    logger.info("Data successfully written to InfluxDB!")

except FileNotFoundError:

    logger.error(f"Error: There is no csv file for: {filename}")


except Exception as e:

    logger.exception(f'An error occured: {str(e)}')
