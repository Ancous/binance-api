import requests
import json


def get_server_time_spot() -> dict:

    """
    Запрос:
    Получить время сервера спота

    Полный url:
    "https://api.binance.com/api/v3/time"

    Вес запроса:
    1

    Параметры:
    - None

    Комментарии:
    - None

    Ответ:
    {
        "serverTime": 1681510841571
    }
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/time"
    # -------------------------------------------

    complete_request = base_url + end_point

    response = requests.get(url=complete_request)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":
    get_server_time_spot()
