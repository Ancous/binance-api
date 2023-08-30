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


def post_market(symbol: str,
                side: str,
                quantity: str,
                time_stamp: str,
                my_type: str = "MARKET",
                new_order_resp_type: str = "RESULT",
                new_client_order_id: str = str(randint(1, 100000)),
                working_type: str = "CONTRACT_PRICE",
                price_protect: str = "FALSE",
                position_side: str = "BOTH",
                recv_window: str = "5000") -> dict:

    """
    Запрос:
    Разместить ордер MARKET

    Полный url:
    "https://fapi.binance.com/fapi/v1/order"

    Вес запроса:
    0

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - side="side" (str): сторона сделки ("BUY", "SELL")
    - quantity="quantity" (str): количества актива в сделки ("16", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - my_type="type" (str): вид ордера ("MARKET")
    - new_order_resp_type="newOrderRespType" (str): развёрнутость ответа ("ACK", "RESULT", "FULL")
    - new_client_order_id="newClientOrderId" (str): идентификатор сделки ("567887", ...)
    - working_type="workingType" (str): ... ("CONTRACT_PRICE", "MARK_PRICE")
    - price_protect="priceProtect" (str): ... ("FALSE", "TRUE")
    - position_side="positionSide" (str): ... ("BOTH", "LONG", "SHORT")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Все аргументы заполняются заглавными буквами
    - минимальное значение "quantity" рассчитывается как (end_point /fapi/v1/exchangeInfo float(["symbols"][если "symbol" == "symbol"]["filters"][если "filterType" == "MIN_NOTIONAL"]["notional"]) / end_point /fapi/v1/ticker/price float(["price"])
    - "side" возможные варианты: ["BUY" - купить, "SELL"- продать]
    - "newOrderRespType" возможные варианты: ["ACK" - короткий ответ, "RESULT" - оптимальный ответ, "FULL" - полный ответ]

    Ответ:
    {
       "orderId": 31424034902,
       "symbol": "ADAUSDT",
       "status": "FILLED",
       "clientOrderId": "87391",
       "price": "0",
       "avgPrice": "0.38270",
       "origQty": "14",
       "executedQty": "14",
       "cumQty": "14",
       "cumQuote": "5.35780",
       "timeInForce": "GTC",
       "type": "MARKET",
       "reduceOnly": false,
       "closePosition": false,  (if Close-All)
       "side": "SELL",
       "positionSide": "BOTH",
       "stopPrice": "0",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
       "workingType": "CONTRACT_PRICE",
       "priceProtect": false,   (if conditional order trigger is protected)
       "origType": "MARKET",
       "updateTime": 1682112737188
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
        "positionSide": position_side,
        "type": my_type,
        "newClientOrderId": new_client_order_id,
        "workingType": working_type,
        "priceProtect": price_protect,
        "newOrderRespType": new_order_resp_type,
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

    post_market(symbol="ADAUSDT", side="BUY", quantity="16.0", time_stamp=str(round(time.time() * 1000)))
