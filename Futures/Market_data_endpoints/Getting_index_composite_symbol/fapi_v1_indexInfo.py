import requests
import json


def get_index_composite_symbol(symbol: str = "") -> dict:

    """
    Запрос:
    Получить информацию о символе составного индекса

    Полный url:
    "https://fapi.binance.com/fapi/v1/indexInfo"

    Вес запроса:
    10

    Параметры:
    - symbol="symbol" (str): актив ("DEFIUSDT", ...)

    Комментарии:
    - Только для символов составного индекса

    Ответ:
    [
        {
            "symbol": "DEFIUSDT",
            "time": 1589437530011,   (текущее время)
            "component": "baseAsset",   (Актив компонента)
            "baseAssetList":[
                {
                    "baseAsset":"BAL",
                    "quoteAsset": "USDT",
                    "weightInQuantity":"1.04406228",
                    "weightInPercentage":"0.02783900"
                },
                {
                    "baseAsset":"BAND",
                    "quoteAsset": "USDT",
                    "weightInQuantity":"3.53782729",
                    "weightInPercentage":"0.03935200"
                }
            ]
        }
    ]
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/indexInfo"
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

    result_2 = get_index_composite_symbol()

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
