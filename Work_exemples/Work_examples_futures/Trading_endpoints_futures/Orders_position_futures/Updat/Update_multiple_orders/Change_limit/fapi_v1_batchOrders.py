"""
pass
"""

import os
import time

from random import randint
from dotenv import load_dotenv

from Futures import TradingEndpointsFutures

load_dotenv()

if __name__ in "__main__":
    client_te = TradingEndpointsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    trades_parameters = [
        ["ADAUSDT", "BUY", "68.0", "0.3100", "32717797178", "74707"],
        ["ADAUSDT", "BUY", "136.0", "0.3050", "32717797177", "14019"],
        ["ADAUSDT", "BUY", "16.0", "0.3696", "857717797177", "55019"],
        ["ADAUSDT", "BUY", "17.0", "0.3596", "3757597177", "75896"],
        ["ADAUSDT", "BUY", "20.0", "0.3496", "96547797177", "45019"]
    ]
    result = client_te.put_multiple_limit_futures(data_list=trades_parameters,
                                                  time_stamp=str(round(time.time() * 1000)))

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
