import requests
import json


def connection_check_spot() -> dict:

    """
    Запрос:
    Проверка соединения спота

    Полный url:
    "https://api.binance.com/api/v3/ping"

    Вес запроса:
    1

    Параметры:
    None

    Комментарии:
    None

    Ответ:
    {}
    """

    # -------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/ping"
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

    connection_check_spot()
