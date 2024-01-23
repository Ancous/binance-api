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
        ["ADAUSDT", "BUY", "14.0", "0.2596", "0.28000090", "BOTH", "TAKE_PROFIT", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "32.0", "0.2596", "0.20000890", "BOTH", "TAKE_PROFIT", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "16.0", "0.2596", "0.28000090", "BOTH", "TAKE_PROFIT", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "17.0", "0.2596", "0.284545490", "BOTH", "TAKE_PROFIT", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "20.0", "0.2596", "0.285454590", "BOTH", "TAKE_PROFIT", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"]
    ]
    result = client.post_multiple_profit_limit_futures(data_list=trades_parameters,
                                                       time_stamp=str(round(time.time() * 1000)))

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
