"""
pass
"""

import os

from dotenv import load_dotenv
from binance_api_ancous import Spot

load_dotenv()

if __name__ in "__main__":

    client = Spot(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    result = client.get_candles_spot(symbol="ADAUSDT", interval="5m")

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
