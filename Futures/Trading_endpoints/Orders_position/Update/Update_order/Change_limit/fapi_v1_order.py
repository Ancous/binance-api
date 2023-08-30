import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()


def put_limit(symbol: str,
              side: str,
              quantity: str,
              price: str,
              time_stamp: str,
              order_id: str = "",
              orig_client_order_id: str = "",
              recv_window: str = "5000") -> dict:

    """
    Запрос:
    Обновить ордер LIMIT

    Полный url:
    "https://fapi.binance.com/fapi/v1/order"

    Вес запроса:
    1

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - side="side" (str): сторона сделки ("BUY", "SELL")
    - quantity="quantity" (str): количества актива в сделки ("16", ...)
    - price="price" (str): по какой цене выставится limit_order ("26234", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - order_id="orderId" (str): самозаполняющимся идентификатор для каждой сделки ("567834287", ...)
    - orig_client_order_id="origClientOrderId" (str): идентификатор сделки  ("567887", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Необходимо обязательно отправить либо order_id, либо orig_client_order_id.
    - orderId имеет преимущественную силу, если отправлены оба.
    - Должны быть отправлены и отличаться от старого заказа или количество или цена.
    - Один заказ может быть изменен не более 10000 раз

    Ответ:
    {
       "orderId": 32717294490,
       "symbol": "ADAUSDT",
       "status": "NEW",
       "clientOrderId": "31699",
       "price": "0.33000",
       "avgPrice": "0.00000",
       "origQty": "17",
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
       "updateTime": 1686133002234
    }
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/order"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "quantity": quantity,
        "price": price,
        "timestamp": time_stamp,
        "orderId": order_id,
        "origClientOrderId": orig_client_order_id,
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

    response = requests.put(url=complete_request, params=complete_parameters, headers=headers)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    put_limit(symbol="ADAUSDT", side="BUY", quantity="17.0", price="0.3300", order_id="32717294490", time_stamp=str(round(time.time() * 1000)))
