import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_open_orders_all(time_stamp: str,
                        symbol: str = "",
                        recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить информацию о всех открытых ордерах

    Полный url:
    "https://fapi.binance.com/fapi/v1/openOrders"

    Вес запроса:
    1 с указанным символом, 40 без указанного символа

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492". ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Если запрошенный заказ был выполнен или отменен, будет возвращено сообщение об ошибке «Order does not exist»
    - Эти заказы не будут найдены:
        - статус заказа CANCELED
        - статус заказа CANCELED EXPIRED
        - ордер не имеет заполненной сделки
        - прошло больше 3-х дней с момента исполнения ордера

    Ответ:
    [
       {
          "orderId": 31449177351,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "51475",
          "price": "0",
          "avgPrice": "0",
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
       },
       {
          "orderId": 31449046574,
          "symbol": "ADAUSDT",
          "status": "NEW",
          "clientOrderId": "1113",
          "price": "0",
          "avgPrice": "0",
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
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/openOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "timestamp": time_stamp,
        "symbol": symbol.upper(),
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

    get_open_orders_all(time_stamp=str(round(time.time() * 1000)))
