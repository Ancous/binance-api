import requests
import json


def get_multiassets(symbol: str = "") -> dict:

    """
    Запрос:
    Получить индекс активов для режима Multi-Assets

    Полный url:
    "https://fapi.binance.com/fapi/v1/assetIndex"

    Вес запроса:
    1 для одного символа, 10 когда параметр символа отсутствует

    Параметры:
    - symbol="symbol" (str): актив ("ADAUSD", ...)

    Комментарии:
    - None

    Ответ:
    {
        "symbol": "ADAUSD",
        "time": 1635740268004,
        "index": "1.92957370",
        "bidBuffer": "0.10000000",
        "askBuffer": "0.10000000",
        "bidRate": "1.73661633",
        "askRate": "2.12253107",
        "autoExchangeBidBuffer": "0.05000000",
        "autoExchangeAskBuffer": "0.05000000",
        "autoExchangeBidRate": "1.83309501",
        "autoExchangeAskRate": "2.02605238"
    }
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/assetIndex"
    parameters = {
        "symbol": symbol.upper(),
    }
    # ---------------------------------------------

    complete_request = base_url + end_point
    complete_parameters = parameters

    response = requests.get(url=complete_request, params=complete_parameters)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_multiassets()

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
