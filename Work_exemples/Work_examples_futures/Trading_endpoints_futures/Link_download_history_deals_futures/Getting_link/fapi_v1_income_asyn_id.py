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
    # result_dop = client.get_id_deals_futures(start_time="16855668000",
    #                                          end_time="16859124000",
    #                                          time_stamp=str(round(time.time() * 1000)))
    result = client.get_link_deals_futures(download_id="1232146453213213",
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
