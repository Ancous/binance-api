import requests
import json
import time
import os
import hmac
import hashlib
from random import randint
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def post_multiple_profit_limit(data_list: list[list[str, ...], ...],
                               time_stamp: str,
                               recv_window: str = "5000") -> dict:

    """
    Запрос:
    Разместить множественный ордер TAKE_PROFIT

    Полный url:
    "https://fapi.binance.com/fapi/v1/batchOrders"

    Вес запроса:
    5

    Параметры:
    - data_list="batchOrders" (list[list[str, ...], ...]): список сделок в строковом формате ("[{"symbol": "ADAUSDT", "side": "BUY", "quantity": "14.0", "price": "0.3896", "stopPrice": "0.4890", "positionSide": "BOTH", "type": "TAKE_PROFIT", "timeInForce": "GTC", "newClientOrderId": "232", "workingType": "CONTRACT_PRICE", "priceProtect": "FALSE", "newOrderRespType": "RESULT"}, {"symbol": "BTCUSDT", "side": "BUY", "quantity": "1.0", "price": "45596", "positionSide": "BOTH", "type": "MARKET", "timeInForce": "GTC", "newClientOrderId": "232112", "workingType": "CONTRACT_PRICE", "priceProtect": "FALSE", "newOrderRespType": "RESULT"}, ...]")
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Максимально можно сделать запрос на 5 ордеров
    - Все данные в списках заполняются заглавными буквами
    - порядок записи данных в data_list: ["symbol", "side", "quantity", "price", "stopPrice", "positionSide", "type", "timeInForce", "newClientOrderId", "workingType", "priceProtect", "newOrderRespType"]
    - возможные варианты записи data_list:  [[<"ADAUSDT">, <"BUY", "SELL">, <"14.0">, <"0.3896">, <"0.4890">, <"BOTH", "LONG", "SHORT">, <"TAKE_PROFIT">, <"GTC", "IOC", "FOK">, <"2312">, <"CONTRACT_PRICE", "MARK_PRICE">, <"FALSE", "TRUE">, <"ACK", "RESULT", "FULL">], ...]

    Ответ:
    [
       {
          "orderId": 31424574628,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "10997",
          "price": "0.25960",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "cumQty": "0",
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TAKE_PROFIT",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0.28900",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TAKE_PROFIT",
          "updateTime": 1682114551241
       },
       {
          "orderId": 31424574629,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "87542",
          "price": "0.25960",
          "avgPrice": "0.00000",
          "origQty": "32",
          "executedQty": "0",
          "cumQty": "0",
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TAKE_PROFIT",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0.28900",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TAKE_PROFIT",
          "updateTime": 1682114551241
       },
       {
          "orderId": 31424574631,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "31299",
          "price": "0.25960",
          "avgPrice": "0.00000",
          "origQty": "16",
          "executedQty": "0",
          "cumQty": "0",
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TAKE_PROFIT",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0.28900",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TAKE_PROFIT",
          "updateTime": 1682114551241
       },
       {
          "orderId": 31424574630,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "11140",
          "price": "0.25960",
          "avgPrice": "0.00000",
          "origQty": "17",
          "executedQty": "0",
          "cumQty": "0",
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TAKE_PROFIT",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0.28900",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TAKE_PROFIT",
          "updateTime": 1682114551241
       },
       {
          "orderId": 31424574632,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "93867",
          "price": "0.25960",
          "avgPrice": "0.00000",
          "origQty": "20",
          "executedQty": "0",
          "cumQty": "0",
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TAKE_PROFIT",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0.28900",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TAKE_PROFIT",
          "updateTime": 1682114551241
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/batchOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")

    list_batch_orders = list()

    key_list = ["symbol", "side", "quantity", "price", "stopPrice", "positionSide", "type", "timeInForce", "newClientOrderId", "workingType", "priceProtect", "newOrderRespType"]

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

    response = requests.post(url=complete_request, data=complete_parameters, headers=headers)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    trades_parameters = [
        ["ADAUhSDT", "BUY", "14.0", "0.2596", "0.28000090", "BOTH", "TAKE_PROFIT", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAhUSDT", "BUY", "32.0", "0.2596", "0.20000890", "BOTH", "TAKE_PROFIT", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUhSDT", "BUY", "16.0", "0.2596", "0.28000090", "BOTH", "TAKE_PROFIT", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUhSDT", "BUY", "17.0", "0.2596", "0.284545490", "BOTH", "TAKE_PROFIT", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAhUSDT", "BUY", "20.0", "0.2596", "0.285454590", "BOTH", "TAKE_PROFIT", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"]
    ]

    post_multiple_profit_limit(data_list=trades_parameters, time_stamp=str(round(time.time() * 1000)))
