import os
import requests
import json

from dotenv import load_dotenv


load_dotenv()


def start_user_data_stream() -> dict:

    """
    Запрос:
    Запустить стрим по данным пользователя

    Полный url:
    "https://fapi.binance.com/fapi/v1/listenKey"

    Вес запроса:
    1

    Параметры:
    None

    Комментарии:
    None

    Ответ:
    {
       "listenKey": "N6Ogns4WQsQdYZ1JfzvqMIQLbx1Q9RKHMbl9vmEOgm4M0kUDxXdbtSejs0fruDsw"
    }
    """

    # -------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/listenKey"
    api_key = os.getenv("api_key")
    # -------------------------------------------

    complete_request = base_url + end_point
    headers = {
        "X-MBX-APIKEY": api_key
    }
    response = requests.post(url=complete_request, headers=headers)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = start_user_data_stream()

    if result_2["status_code"] == 200:
        print("status_code:" ,result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
