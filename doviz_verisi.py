import requests

API_URL = "https://api.exchangerate-api.com/v4/history/USD/2025/01/01"

def get_exchange_rates():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data["rates"]

    else:
        print("Döviz kuru verisi alınamadı.")
        return None

if __name__ == "__main__":
    rates = get_exchange_rates()
    if rates:
        print("Güncel Döviz Kurları:", rates)
