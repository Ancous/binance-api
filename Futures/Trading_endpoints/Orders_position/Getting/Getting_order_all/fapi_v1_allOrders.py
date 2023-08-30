import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_orders_all(symbol: str,
                   time_stamp: str,
                   order_id: str = "",
                   start_time: str = "",
                   end_time: str = "",
                   limit: str = "500",
                   recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить информацию о всех ордерах аккаунта

    Полный url:
    "https://fapi.binance.com/fapi/v1/allOrders"

    Вес запроса:
    5

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - order_id="orderId" (str): самозаполняющимся идентификатор для каждой сделки ("567834287", ...)
    - start_time="startTime" (str): время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): какое количество ордеров вывести ("5", ..., "1000")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - order_id является самозаполняющимся для каждого конкретного символа
    - Если установлен "orderId", он выведет ордера позже этого "orderId" включительно. В противном случае будут возвращены самые последние заказы.
    - Период между "startTime" и  "endTime" должен быть меньше 7 дней (по умолчанию последние 7 дней).

    Ответ:
    [
       {
          "orderId": 31449046574,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "1113",
          "price": "0",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "activatePrice": "0.30970",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "reduceOnly": false,
          "closePosition": false,   (if Close-All)
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0.39945",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TRAILING_STOP_MARKET",
          "time": 1682190044181,   (время создания ордера)
          "updateTime": 1682190044181   (последние время взаимодействия с ордером)
       },
       {
          "orderId": 31449177351,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "51475",
          "price": "0",
          "avgPrice": "0.00000",
          "origQty": "14",
          "executedQty": "0",
          "activatePrice": "0.30970",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "priceRate": "1.0",   (в ответе только если ордер TRAILING_STOP_MARKET)
          "cumQuote": "0",
          "timeInForce": "GTC",
          "type": "TRAILING_STOP_MARKET",
          "reduceOnly": false,
          "closePosition": false,   (if Close-All)
          "side": "BUY",
          "positionSide": "BOTH",
          "stopPrice": "0.39915",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
          "workingType": "CONTRACT_PRICE",
          "priceProtect": false,   (if conditional order trigger is protected)
          "origType": "TRAILING_STOP_MARKET",
          "time": 1682190400946,   (время создания ордера)
          "updateTime": 1682190400946   (последние время взаимодействия с ордером)
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/allOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "orderId": order_id,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
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
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    get_orders_all(symbol="ADAUSDT", order_id="31449046574", time_stamp=str(round(time.time() * 1000)))
