"""
pass
"""

import os
import json
import time

from random import randint
from dotenv import load_dotenv
from binance_api_ancous import Futures

load_dotenv()

if __name__ in "__main__":
    client = Futures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    trades_parameters = [
        ["ADAUSDT", "BUY", "14.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "15.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "16.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "17.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "18.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"]
    ]
    result = client.post_multiple_market_futures(data_list=trades_parameters,
                                                 time_stamp=str(round(time.time() * 1000)))
    with open("answer.json", "w") as file:
        json.dump(obj=result["result"], fp=file, indent=3)

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
