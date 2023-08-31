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


def post_profit_market(symbol: str,
                       side: str,
                       quantity: str,
                       stop_price: str,
                       time_stamp: str,
                       my_type: str = "TAKE_PROFIT_MARKET",
                       time_in_force: str = "GTC",
                       new_order_resp_type: str = "RESULT",
                       new_client_order_id: str = str(randint(1, 100000)),
                       reduce_only: str = "FALSE",
                       close_position: str = "FALSE",
                       working_type: str = "CONTRACT_PRICE",
                       price_protect: str = "FALSE",
                       position_side: str = "BOTH",
                       recv_window: str = "5000") -> dict:

    """
    Запрос:
    Разместить ордер TAKE_PROFIT_MARKET

    Полный url:
    "https://fapi.binance.com/fapi/v1/order"

    Вес запроса:
    0

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - side="side" (str): сторона сделки ("BUY", "SELL")
    - quantity="quantity" (str): количества актива в сделки ("16", ...)
    - stop_price="stopPrice" (str): по какой цене разместится profit_order ("268234", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - my_type="type" (str): вид ордера ("TAKE_PROFIT_MARKET")
    - time_in_force="timeInForce" (str): режим исполнения ("GTC", "IOC", "FOK", "GTD", "GTX")
    - new_order_resp_type="newOrderRespType" (str): развёрнутость ответа ("ACK", "RESULT", "FULL")
    - new_client_order_id="newClientOrderId" (str): идентификатор сделки ("567887", ...)
    - reduce_only="reduceOnly" (str): ... ("FALSE", "TRUE")
    - close_position="closePosition" (str): ... ("FALSE", "TRUE")
    - working_type="workingType" (str): ... ("CONTRACT_PRICE", "MARK_PRICE")
    - price_protect="priceProtect" (str): ... ("FALSE", "TRUE")
    - position_side="positionSide" (str): ... ("BOTH", "LONG", "SHORT")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Все аргументы заполняются заглавными буквами
    - минимальное значение "quantity" рассчитывается как (end_point /fapi/v1/exchangeInfo float(["symbols"][если "symbol" == "symbol"]["filters"][если "filterType" == "MIN_NOTIONAL"]["notional"]) / end_point /fapi/v1/ticker/price float(["price"])
    - "side" возможные варианты: ["BUY" - купить, "SELL"- продать]
    - "stop_price" используется если "type" == ("STOP", "STOP_MARKET", "TAKE_PROFIT", "TAKE_PROFIT_MARKET")
    - "timeInForce" возможные варианты: ["GTC" – ордер будет висеть до тех пор, пока его не отменят, "IOC" – будет куплено то количество, которое можно купить немедленно. Все, что не удалось купить, будет отменено, "FOK" – либо будет куплено все указанное количество немедленно, либо не будет куплено вообще ничего, ордер отменится, "GTD" - до определённой даты или до конца дня, "GTX" - ....
    - "reduceOnly" не может быть отправлен в режиме хеджирования так же нельзя отправить с параметром closePosition="True"
    - "newOrderRespType" возможные варианты: ["ACK" - короткий ответ, "RESULT" - оптимальный ответ, "FULL" - полный ответ]
    - если "side" == "BUY", то "stopPrice" должен быть меньше end_point /fapi/v1/ticker/price float(["price"])
    - если "side" == "SELL", то "stopPrice" должен быть больше end_point /fapi/v1/ticker/price float(["price"])

    Ответ:
    {
       "orderId": 31424170469,
       "symbol": "ADAUSDT",
       "status": "NEW",
       "clientOrderId": "46901",
       "price": "0",
       "avgPrice": "0.00000",
       "origQty": "13",
       "executedQty": "0",
       "cumQty": "0",
       "cumQuote": "0",
       "timeInForce": "GTC",
       "type": "TAKE_PROFIT_MARKET",
       "reduceOnly": false,
       "closePosition": false,   (if Close-All)
       "side": "BUY",
       "positionSide": "BOTH",
       "stopPrice": "0.30000",   (пожалуйста, игнорируйте, если тип ордера TRAILING_STOP_MARKET)
       "workingType": "CONTRACT_PRICE",
       "priceProtect": false,   (if conditional order trigger is protected)
       "origType": "TAKE_PROFIT_MARKET",
       "updateTime": 1682113177309
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
        "stopPrice": stop_price,
        "positionSide": position_side,
        "type": my_type,
        "timeInForce": time_in_force,
        "reduceOnly": reduce_only,
        "newClientOrderId": new_client_order_id,
        "closePosition": close_position,
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

    post_profit_market(symbol="ADAUSDT", side="BUY", quantity="15.0", stop_price="0.3000", time_stamp=str(round(time.time() * 1000)))
