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


def post_multiple_trailing_stop_market(data_list: list[list[str, ...], ...],
                                       time_stamp: str,
                                       recv_window: str = "5000") -> list | str:

    """
    Запрос:
    Разместить множественный ордер TRAILING_STOP_MARKET

    Полный url:
    "https://fapi.binance.com/fapi/v1/batchOrders"

    Вес запроса:
    5

    Параметры:
    - data_list="batchOrders" (list[list[str, ...], ...]): список сделок в строковом формате ("[{"symbol": "ADAUSDT", "side": "BUY", "quantity": "14.0", "activationPrice": "0.4450", "callbackRate": "1.0", "positionSide": "BOTH", "type": "TRAILING_STOP_MARKET", "timeInForce": "GTC", "newClientOrderId": "232", "workingType": "CONTRACT_PRICE", "newOrderRespType": "RESULT"}, {"symbol": "ADAUSDT", "side": "BUY", "quantity": "14.0", "activationPrice": "0.4450", "callbackRate": "1.0", "positionSide": "BOTH", "type": "TRAILING_STOP_MARKET", "timeInForce": "GTC", "newClientOrderId": "232", "workingType": "CONTRACT_PRICE", "newOrderRespType": "RESULT"}, ...]")
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Максимально можно сделать запрос на 5 ордеров
    - Все данные в списках заполняются заглавными буквами
    - порядок записи данных в data_list: ["symbol", "side", "quantity", "activationPrice", "callbackRate", "positionSide", "type", "timeInForce", "newClientOrderId", "workingType", "newOrderRespType"]
    - возможные варианты записи data_list:  [[<"ADAUSDT">, <"BUY", "SELL">, <"14.0">, <"0.4450"> ,<"0.1", "0.2", "0.3", ..., "5.0"> , <"BOTH", "LONG", "SHORT">, <"TRAILING_STOP_MARKET">, <"GTC", "IOC", "FOK">, <"2312">, <"CONTRACT_PRICE", "MARK_PRICE">, <"ACK", "RESULT", "FULL">], ...]

    Ответ:
    [
       {
          "orderId": 31424714051,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "43160",
          "price": "0",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "cumQty": "0",
          "activatePrice": "0.30900",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TRAILING_STOP_MARKET",
          "updateTime": 1682115046384
       },
       {
          "orderId": 31424714049,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "34698",
          "price": "0",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "cumQty": "0",
          "activatePrice": "0.30800",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TRAILING_STOP_MARKET",
          "updateTime": 1682115046384
       },
       {
          "orderId": 31424714048,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "8144",
          "price": "0",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "cumQty": "0",
          "activatePrice": "0.30700",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TRAILING_STOP_MARKET",
          "updateTime": 1682115046384
       },
       {
          "orderId": 31424714047,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "28876",
          "price": "0",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "cumQty": "0",
          "activatePrice": "0.30600",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TRAILING_STOP_MARKET",
          "updateTime": 1682115046384
       },
       {
          "orderId": 31424714050,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "73655",
          "price": "0",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "cumQty": "0",
          "activatePrice": "0.30500",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TRAILING_STOP_MARKET",
          "updateTime": 1682115046384
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/batchOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")

    list_batch_orders = list()

    key_list = ["symbol", "side", "quantity", "activationPrice", "callbackRate", "positionSide", "type", "timeInForce", "newClientOrderId", "workingType", "newOrderRespType"]

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
        return result
    else:
        error = f"ОШИБКА!!!\nСтатус-код ответа: {response.status_code}\nКод ошибки: {result['code']}\nТекст ошибки: {result['msg']}"
        return error


if __name__ in "__main__":

    trades_parameters = [
        ["ADAUSDT", "BUY", "14.0", "0.3090", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3080", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3070", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3060", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"],
        ["ADAUSDT", "BUY", "14.0", "0.3050", "1.0", "BOTH", "TRAILING_STOP_MARKET", "GTC", str(randint(1, 100000)), "CONTRACT_PRICE", "RESULT"]
    ]

    post_multiple_trailing_stop_market(data_list=trades_parameters, time_stamp=str(round(time.time() * 1000)))
