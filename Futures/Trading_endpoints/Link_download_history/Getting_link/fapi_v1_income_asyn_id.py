import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_link(download_id: str,
             time_stamp: str,
             recv_window: str = "5000") -> dict:

    """
    Запрос:
    Получить ссылку для скачивания истории сделок с фьючерсами по идентификатору

    Полный url:
    "https://fapi.binance.com/fapi/v1/income/asyn/id"

    Вес запроса:
    5

    Параметры:
    - download_id="downloadId" (str): идентификатор загрузки ("132131234", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - "downloadId" можно получит по url "https://fapi.binance.com/fapi/v1/income/asyn"
    - Срок действия ссылки для скачивания: 24 часа

    Ответ:
    - Если результат ответ завершен ("completed"):

    {
       "downloadId": "705897285947772928",
       "status": "completed",   ("completed"-завершено или "processing"-обработка)
       "url": "https://bin-prod-user-rebate-bucket.s3.amazonaws.com/data-download-task/usdt_margined_futures/2023-05-02/b11da5e4-e932-11ed-b29b-06d1fef09917/202305022143.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVL364M5ZE4RJPUCE%2F20230502%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20230502T214746Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=891df982df2e66c63f6e6ceda3e0d23ab078e89d58f13372e6f750271fae5c1a",   (Ссылка сопоставлена с идентификатором загрузки)
       "s3Link": null,
       "notified": true,   (ignore)
       "expirationTimestamp": 1683668866000,   (Срок действия ссылки истекает после этой метки времени)
       "isExpired": null
    }

    - Если результат ответ в обработке ("processing"):

    {
        "downloadId":"545923594199212032",
        "status":"completed",   ("completed"-завершено или "processing"-обработка))
        "url":"www.binance.com",   (Срок действия ссылки истекает после этой метки времени)
        "notified":true,   (ignore)
        "expirationTimestamp":1645009771000,   (Срок действия ссылки истекает после этой метки времени)
        "isExpired":null,
    }
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/income/asyn/id"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "downloadId": download_id,
        "timestamp": time_stamp,
        "recvWindow": recv_window
    }
    query_string = urlencode(parameters)
    parameters["signature"] = hmac.new(key=secret_key.encode(),
                                       msg=query_string.encode(),
                                       digestmod=hashlib.sha256).hexdigest()
    # -------------------------------------------------------------------------

    complete_request = base_url + end_point
    complete_parameters = parameters
    headers = {
        "X-MBX-APIKEY": api_key
    }

    response = requests.get(url=complete_request, params=complete_parameters, headers=headers)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_link(download_id="705897285947772928", time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
