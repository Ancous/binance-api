"""
pass
"""

import os
import time

from dotenv import load_dotenv

from Futures import TradingEndpointsFutures

load_dotenv()

if __name__ in "__main__":
    client_te = TradingEndpointsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    result = client_te.post_limit_futures(symbol="ADAUSDT",
                                          side="BUY",
                                          quantity="25.0",
                                          price="0.2000",
                                          time_stamp=str(round(time.time() * 1000)))

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
