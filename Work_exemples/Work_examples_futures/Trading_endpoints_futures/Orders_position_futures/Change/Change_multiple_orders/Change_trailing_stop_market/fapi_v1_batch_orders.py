"""
pass
"""

import os
import time

from random import randint
from dotenv import load_dotenv
from binance_api_ancous import Futures

load_dotenv()

if __name__ in "__main__":
    client = Futures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    trades_parameters = [
        ["ADAUSDT", "BUY", "14.0", "0.3090", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3080", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3070", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3060", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3050", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"]
    ]
    result = client.post_multiple_trailing_stop_market_futures(data_list=trades_parameters,
                                                               time_stamp=str(round(time.time() * 1000)))

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
