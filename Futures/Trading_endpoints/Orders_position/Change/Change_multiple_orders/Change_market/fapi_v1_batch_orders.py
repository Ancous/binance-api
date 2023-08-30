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


def post_multiple_market(data_list: list[list[str, ...], ...],
                         time_stamp: str,
                         recv_window: str = "5000") -> dict:

    """
    Запрос:
    Разместить множественный ордер MARKER

    Полный url:
    "https://fapi.binance.com/fapi/v1/batchOrders"

    Вес запроса:
    5

    Параметры:
    - data_list="batchOrders" (list[list[str, ...], ...]): список сделок в строковом формате ("[{"symbol": "ADAUSDT", "side": "BUY", "quantity": "14.0", "positionSide": "BOTH", "type": "LIMIT", "newClientOrderId": "232", "workingType": "CONTRACT_PRICE", "priceProtect": "FALSE", "newOrderRespType": "RESULT"}, {"symbol": "BTCUSDT", "side": "BUY", "quantity": "1.0", "price": "45596", "positionSide": "BOTH", "type": "MARKET", "timeInForce": "GTC", "newClientOrderId": "232112", "workingType": "CONTRACT_PRICE", "priceProtect": "FALSE", "newOrderRespType": "RESULT"}, ...]")
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - "recvWindow"=recv_window (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Максимально можно сделать запрос на 5 ордеров
    - Все данные в списках заполняются заглавными буквами
    - порядок записи данных в data_list: ["symbol", "side", "quantity", "positionSide", "type", "newClientOrderId", "workingType", "priceProtect", "newOrderRespType"]
    - возможные варианты записи data_list:  [[<"ADAUSDT">, <"BUY", "SELL">, <"14.0">, <"BOTH", "LONG", "SHORT">, <"MARKER">, <"2312">, <"CONTRACT_PRICE", "MARK_PRICE">, <"FALSE", "TRUE">, <"ACK", "RESULT", "FULL">], ...]

    Ответ:
    [
       {
          "orderId": 31424464263,
          "symbol": "ADAUSDT",
          "status": "FILLED",
          "clientOrderId": "74133",
          "price": "0",
          "avgPrice": "0.38030",
          "origQty": "14",
          "executedQty": "14",
          "cumQty": "14",
          "cumQuote": "5.32420",
          "timeInForce": "GTC",
          "type": "MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "MARKET",
          "updateTime": 1682114212682
       },
       {
          "orderId": 31424464264,
          "symbol": "ADAUSDT",
          "status": "FILLED",
          "clientOrderId": "76171",
          "price": "0",
          "avgPrice": "0.38030",
          "origQty": "15",
          "executedQty": "15",
          "cumQty": "15",
          "cumQuote": "5.70450",
          "timeInForce": "GTC",
          "type": "MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "MARKET",
          "updateTime": 1682114212682
       },
       {
          "orderId": 31424464265,
          "symbol": "ADAUSDT",
          "status": "FILLED",
          "clientOrderId": "74342",
          "price": "0",
          "avgPrice": "0.38030",
          "origQty": "16",
          "executedQty": "16",
          "cumQty": "16",
          "cumQuote": "6.08480",
          "timeInForce": "GTC",
          "type": "MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "MARKET",
          "updateTime": 1682114212682
       },
       {
          "orderId": 31424464266,
          "symbol": "ADAUSDT",
          "status": "FILLED",
          "clientOrderId": "98485",
          "price": "0",
          "avgPrice": "0.38030",
          "origQty": "17",
          "executedQty": "17",
          "cumQty": "17",
          "cumQuote": "6.46510",
          "timeInForce": "GTC",
          "type": "MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "MARKET",
          "updateTime": 1682114212682
       },
       {
          "orderId": 31424464267,
          "symbol": "ADAUSDT",
          "status": "FILLED",
          "clientOrderId": "56364",
          "price": "0",
          "avgPrice": "0.38030",
          "origQty": "18",
          "executedQty": "18",
          "cumQty": "18",
          "cumQuote": "6.84540",
          "timeInForce": "GTC",
          "type": "MARKET",
          "reduceOnly": false,
          "closePosition": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "MARKET",
          "updateTime": 1682114212682
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/batchOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")

    list_batch_orders = list()

    key_list = ["symbol", "side", "quantity", "positionSide", "type", "newClientOrderId", "workingType", "priceProtect", "newOrderRespType"]

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
        ["ADAUSDT", "BUY", "14.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "15.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "16.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "17.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"],
        ["ADAUSDT", "BUY", "18.0", "BOTH", "MARKET", str(randint(1, 100000)), "CONTRACT_PRICE", "FALSE", "RESULT"]
    ]

    post_multiple_market(data_list=trades_parameters, time_stamp=str(round(time.time() * 1000)))
