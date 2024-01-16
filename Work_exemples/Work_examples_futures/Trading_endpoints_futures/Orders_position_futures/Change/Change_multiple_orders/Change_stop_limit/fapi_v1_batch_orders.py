"""
pass
"""

import os
import time

from random import randint
from dotenv import load_dotenv

from binance_api_ancous import TradingEndpointsFutures

load_dotenv()

if __name__ in "__main__":
    client_te = TradingEndpointsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    trades_parameters = [
        ["ADAUSDT", "BUY", "14.0", "0.3896", "0.4890", "BOTH", "STOP", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "32.0", "0.3796", "0.4890", "BOTH", "STOP", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "16.0", "0.3696", "0.4890", "BOTH", "STOP", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "17.0", "0.3596", "0.4890", "BOTH", "STOP", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "20.0", "0.3496", "0.4890", "BOTH", "STOP", "GTC",
         str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"]
    ]
    result = client_te.post_multiple_stop_limit_futures(data_list=trades_parameters,
                                                        time_stamp=str(round(time.time() * 1000)))

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
