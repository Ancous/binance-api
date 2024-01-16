"""
pass
"""

import os
from dotenv import load_dotenv

from binance_api_ancous import MarketDataEndpointsFutures

load_dotenv()

if __name__ in "__main__":

    client_mde = MarketDataEndpointsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    result = client_mde.get_latest_price_futures()

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
