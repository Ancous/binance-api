"""
pass
"""

import os

from dotenv import load_dotenv

from Futures import UserDataStreamsFutures

load_dotenv()


if __name__ in "__main__":

    client_uds = UserDataStreamsFutures(secret_key=os.getenv("secret_key"), api_key=os.getenv("api_key"))
    result = client_uds.delete_user_data_stream_futures()

    if result["status_code"] == 200:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
    else:
        print("status_code:", result["status_code"])
        print("result:", result["result"])
        print("headers:", result["headers"])
