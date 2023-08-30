import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_force_orders(time_stamp: str,
                     symbol: str = "",
                     auto_close_type: str = "",
                     start_time: str = "",
                     end_time: str = "",
                     limit: str = "50",
                     recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить принудительные сделки

    Полный url:
    "https://fapi.binance.com/fapi/v1/forceOrders"

    Вес запроса:
    10 с указанным "symbol", 50 без указанного

    Параметры:
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - auto_close_type="autoCloseType" (str): ... ("LIQUIDATION", "ADL")
    - start_time="startTime" (str): время начала отбора ("1681505080619", ...)
    - end_time="endTime" (str): время окончания отбора ("1681505034619", ...)
    - limit="limit" (str): выводимое количество ("5", ..., "100")
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Если "autoCloseType" не отправлен, будут возвращены ордера с обоими типами
    - Если «startTime» не отправлено, можно запросить данные за 7 дней до «endTime».

    Ответ:
    [
      {
        "orderId": 6071832819,
        "symbol": "BTCUSDT",
        "status": "FILLED",
        "clientOrderId": "autoclose-1596107620040000020",
        "price": "10871.09",
        "avgPrice": "10913.21000",
        "origQty": "0.001",
        "executedQty": "0.001",
        "cumQuote": "10.91321",
        "timeInForce": "IOC",
        "type": "LIMIT",
        "reduceOnly": false,
        "closePosition": false,
        "side": "SELL",
        "positionSide": "BOTH",
        "stopPrice": "0",
        "workingType": "CONTRACT_PRICE",
        "origType": "LIMIT",
        "time": 1596107620044,
        "updateTime": 1596107620087
      }
      {
        "orderId": 6072734303,
        "symbol": "BTCUSDT",
        "status": "FILLED",
        "clientOrderId": "adl_autoclose",
        "price": "11023.14",
        "avgPrice": "10979.82000",
        "origQty": "0.001",
        "executedQty": "0.001",
        "cumQuote": "10.97982",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "reduceOnly": false,
        "closePosition": false,
        "side": "BUY",
        "positionSide": "SHORT",
        "stopPrice": "0",
        "workingType": "CONTRACT_PRICE",
        "origType": "LIMIT",
        "time": 1596110725059,
        "updateTime": 1596110725071
      }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/forceOrders"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "timestamp": time_stamp,
        "symbol": symbol.upper(),
        "autoCloseType": auto_close_type,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
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
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_force_orders(time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
