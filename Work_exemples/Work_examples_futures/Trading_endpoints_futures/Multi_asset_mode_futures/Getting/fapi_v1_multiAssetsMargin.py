"""
pass
"""

import os
import time

from dotenv import load_dotenv

from binance_api_ancous import TradingEndpointsFutures

load_dotenv()

if __name__ in "__main__":

    client_te = TradingEndpointsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    result = client_te.get_multi_asset_futures(time_stamp=str(round(time.time() * 1000)))

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
