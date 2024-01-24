"""
pass
"""

import os
import json
import time

from dotenv import load_dotenv
from binance_api_ancous import Futures

load_dotenv()

if __name__ in "__main__":
    client = Futures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    result = client.delete_multiple_order_id_futures(symbol="ADAUSDT",
                                                     order_id_list=["567887", "567587", "557887", "557887"],
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
