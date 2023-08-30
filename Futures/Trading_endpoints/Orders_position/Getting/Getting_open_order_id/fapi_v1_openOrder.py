import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_open_order_id(symbol: str,
                      time_stamp: str,
                      order_id: str = "",
                      orig_client_order_id: str = "",
                      recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить информацию об открытом ордере по идентификатору

    Полный url:
    "https://fapi.binance.com/fapi/v1/openOrder"

    Вес запроса:
    1

    Параметры:
    - "symbol"=symbol (str): актив ("BTCUSDT", ...)
    - "timestamp"=time_stamp (str): время отправки запроса ("1681501516492", ...)
    - "orderId"=order_id (str): самозаполняющимся идентификатор для каждой сделки ("567834287", ...)
    - "origClientOrderId"=orig_client_order_id (str): идентификатор сделки  ("567887", ...)
    - "recvWindow"=recv_window (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Необходимо обязательно отправить либо order_id, либо orig_client_order_id
    - order_id является самозаполняющимся для каждого конкретного символа
    - Если запрошенный заказ был выполнен или отменен, будет возвращено сообщение об ошибке «Order does not exist»
    - Эти заказы не будут найдены:
        - статус заказа CANCELED
        - статус заказа CANCELED EXPIRED
        - ордер не имеет заполненной сделки
        - прошло больше 3-х дней с момента исполнения ордера

    Ответ:
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
    }
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/openOrder"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "orderId": order_id,
        "origClientOrderId": orig_client_order_id,
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

    get_open_order_id(symbol="ADAUSDT", order_id="31449177351", time_stamp=str(round(time.time() * 1000)))
