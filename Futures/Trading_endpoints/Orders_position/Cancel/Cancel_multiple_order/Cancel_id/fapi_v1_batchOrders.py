import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def delete_multiple_order_id(symbol: str,
                             time_stamp: str,
                             order_id_list: list[str] = (),
                             orig_client_order_id_list: list[str] = (),
                             recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Закрыть несколько ордеров по идентификатору

    Полный url:
    "https://fapi.binance.com/fapi/v1/batchOrders"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - order_id_list="orderIdList" list(str): самозаполняющимся идентификатор для каждой сделки (["567834287", ...])
    - orig_client_order_id_list="origClientOrderIdList" list(str): идентификатор сделки  (["567887", ...])
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Максимально можно передать 10 идентификаторов
    - Закрывает ордера, не открытые позиции!!!
    - Необходимо обязательно отправить либо order_id, либо orig_client_order_id
    - order_id является самозаполняющимся для каждого конкретного символа

    Ответ:
    [
       {
          "clientOrderId": "72017",
          "cumQty": "0",
          "cumQuote": "0",
          "executedQty": "0",
          "orderId": 31425437277,
          "origQty": "14",
          "price": "0",
          "reduceOnly": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "status": "CANCELED",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "symbol": "ADAUSDT",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "updateTime": 1682117738301,
          "avgPrice": "0.00000",
          "workingType": "CONTRACT_PRICE",
          "origType": "TRAILING_STOP_MARKET",
          "activatePrice": "0.30900",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "closePosition": false,   (if Close-All)
          "priceProtect": false   (if conditional order trigger is protected)
       },
       {
          "clientOrderId": "78581",
          "cumQty": "0",
          "cumQuote": "0",
          "executedQty": "0",
          "orderId": 31425437280,
          "origQty": "14",
          "price": "0",
          "reduceOnly": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "status": "CANCELED",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "symbol": "ADAUSDT",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "updateTime": 1682117738301,
          "avgPrice": "0.00000",
          "workingType": "CONTRACT_PRICE",
          "origType": "TRAILING_STOP_MARKET",
          "activatePrice": "0.30800",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "closePosition": false,   (if Close-All)
          "priceProtect": false   (if conditional order trigger is protected)
       },
       {
          "clientOrderId": "39333",
          "cumQty": "0",
          "cumQuote": "0",
          "executedQty": "0",
          "orderId": 31425437278,
          "origQty": "14",
          "price": "0",
          "reduceOnly": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "status": "CANCELED",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "symbol": "ADAUSDT",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "updateTime": 1682117738301,
          "avgPrice": "0.00000",
          "workingType": "CONTRACT_PRICE",
          "origType": "TRAILING_STOP_MARKET",
          "activatePrice": "0.30700",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "closePosition": false,   (if Close-All)
          "priceProtect": false   (if conditional order trigger is protected)
       },
       {
          "clientOrderId": "74115",
          "cumQty": "0",
          "cumQuote": "0",
          "executedQty": "0",
          "orderId": 31425437279,
          "origQty": "14",
          "price": "0",
          "reduceOnly": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "status": "CANCELED",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "symbol": "ADAUSDT",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "updateTime": 1682117738301,
          "avgPrice": "0.00000",
          "workingType": "CONTRACT_PRICE",
          "origType": "TRAILING_STOP_MARKET",
          "activatePrice": "0.30600",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "closePosition": false,   (if Close-All)
          "priceProtect": false   (if conditional order trigger is protected)
       },
       {
          "clientOrderId": "95436",
          "cumQty": "0",
          "cumQuote": "0",
          "executedQty": "0",
          "orderId": 31425437276,
          "origQty": "14",
          "price": "0",
          "reduceOnly": false,
          "side": "BUY",
          "positionSide": "BOTH",
          "status": "CANCELED",
          "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "symbol": "ADAUSDT",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "updateTime": 1682117738301,
          "avgPrice": "0.00000",
          "workingType": "CONTRACT_PRICE",
          "origType": "TRAILING_STOP_MARKET",
          "activatePrice": "0.30500",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "closePosition": false,   (if Close-All)
          "priceProtect": false   (if conditional order trigger is protected)
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/batchOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "orderIdList": json.dumps(order_id_list).replace(" ", ""),
        "origClientOrderIdList": json.dumps(orig_client_order_id_list).replace(" ", ""),
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

    response = requests.delete(url=complete_request, params=complete_parameters, headers=headers)
    result = json.loads(response.text)
    
    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    delete_multiple_order_id(symbol="ADAUSDT", time_stamp=str(round(time.time() * 1000)))
