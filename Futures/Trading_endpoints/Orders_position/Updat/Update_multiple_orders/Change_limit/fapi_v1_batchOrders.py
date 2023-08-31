import requests
import json
import time
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def put_multiple_limit(data_list: list[list[str, ...], ...],
                       time_stamp: str,
                       recv_window: str = "5000") -> dict:

    """
    Запрос:
    Обновить несколько ордеров LIMIT

    Полный url:
    "https://fapi.binance.com/fapi/v1/batchOrders"

    Вес запроса:
    5

    Параметры:
    - data_list="batchOrders" (list[list[str, ...], ...]): список изменяемых ордеров в строковом формате ("[{"symbol": "ADAUSDT", "side": "BUY", "quantity": "14.0", "price": "0.3896", "orderId": "159756485", "origClientOrderId": "12854"}, {"symbol": "ADAUSDT", "side": "BUY", "quantity": "14.0", "price": "0.3896", "orderId": "45698521", "origClientOrderId": "75854"}, ...]")
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - порядок записи данных в data_list: ["symbol", "side", "quantity", "price", "orderId", "origClientOrderId"]
    - возможные варианты записи data_list:  [[<"ADAUSDT">, <"BUY", "SELL">, <"14.0">, <"0.3896">, <"15651651">, <"45874">], ...]
    - Один заказ может быть изменен не более 10000 раз

    Ответ:
    [
       {
          "orderId": 32717797178,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "74707",
          "price": "0.31000",
          "avgPrice": "0.00000",
          "origQty": "68",
          "executedQty": "0",
          "cumQty": "0",
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "LIMIT",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,
          "origType": "LIMIT",
          "updateTime": 1686134330079
       },
       {
          "orderId": 32717797177,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "14019",
          "price": "0.30500",
          "avgPrice": "0.00000",
          "origQty": "136",
          "executedQty": "0",
          "cumQty": "0",
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "LIMIT",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,
          "origType": "LIMIT",
          "updateTime": 1686134330079
       }
    ]

    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/batchOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")

    list_batch_orders = list()

    key_list = ["symbol", "side", "quantity", "price", "orderId", "origClientOrderId"]

    for count, values_list in enumerate(data_list):
        result_list = dict(zip(key_list, values_list))
        list_batch_orders.append(result_list)

    parameters = {
        "batchOrders": json.dumps(list_batch_orders),
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

    response = requests.put(url=complete_request, data=complete_parameters, headers=headers)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    trades_parameters = [
        ["ADAUSDT", "BUY", "68.0", "0.3100", "32717797178", "74707"],
        ["ADAUSDT", "BUY", "136.0", "0.3050", "32717797177", "14019"],
        ["ADAUSDT", "BUY", "16.0", "0.3696", "857717797177", "55019"],
        ["ADAUSDT", "BUY", "17.0", "0.3596", "3757597177", "75896"],
        ["ADAUSDT", "BUY", "20.0", "0.3496", "96547797177", "45019"]
    ]

    put_multiple_limit(data_list=trades_parameters, time_stamp=str(round(time.time() * 1000)))
