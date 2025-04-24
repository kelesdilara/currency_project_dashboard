# 💱 Exchange Rate Monitoring and Visualization System

This project fetches exchange rate data from the European Central Bank (ECB), stores it in InfluxDB, and visualizes it using Grafana. The entire infrastructure is deployed using Docker Compose for easy setup.

## 🧰 Technologies Used

- Docker & Docker Compose  
- InfluxDB  
- Grafana  
- Python  
- Bash  
- Environment variables via `.env` file

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kelesdilara/currency_project_dashboard.git
cd dovizProjesi
```
### 2. Set Up Environment Variables

Create a .env file and add the following:

INFLUXDB_URL=http://localhost:8086  
INFLUXDB_TOKEN=your_token_here  
INFLUXDB_ORG=your_org  
INFLUXDB_BUCKET=dovizdb

### 3. Start Docker Services

```bash
docker-compose up -d
```
- InfluxDB: http://localhost:8086  
- Grafana: http://localhost:3000  

# 📈 Fetch and Store Data
### 1. Run the Script
```bash
bash get_data.sh
```
When executed, the script will prompt you to enter currency codes (e.g., USD TRY SEK). Then it will:

- Download XML files from the ECB
- Convert them to CSV
- Use the Python script to insert the data into InfluxDB
- Delete the temporary CSV and XML files

### 2. Create a Dashboard in Grafana
After logging in to Grafana:
1. Add InfluxDB as a data source
2. Set Bucket to: dovizdb
3. Create panels using the measurement name: eur_exchange_<currency>

# 🗃️ Project Structure

```bash
.
├── docker-compose.yml
├── get_data.sh
├── data_handler.py
├── logger.py
├── .env
├── .gitignore
└── README.md

```
# Developer Notes

- Data is written to InfluxDB using the `influxdb_client` library.
- A custom logging module is implemented in `logger.py`.
- CSV parsing and timestamp formatting are done using Python's `datetime` module.


## Grafana dashboard

![Screenshot](/imagine/img.png)

