import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_current_position_symbol(symbol: str,
                                time_stamp: str,
                                recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить информацию о текущей позиции по символу

    Полный url:
    "https://fapi.binance.com/fapi/v2/positionRisk"

    Вес запроса:
    5

    Параметры:
    - symbol="symbol" (str): актив ("BTCUSDT", ...)
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - Пожалуйста, используйте с потоком пользовательских данных ACCOUNT_UPDATE, чтобы получать данные своевременно и точно.

    Ответ:
    - Для режима односторонней-позиции:

    [
       {
          "symbol": "ADAUSDT",
          "positionAmt": "-14",
          "entryPrice": "0.3842",
          "markPrice": "0.38440335",
          "unRealizedProfit": "-0.00284690",
          "liquidationPrice": "0.57337452",
          "leverage": "2",
          "maxNotionalValue": "30000000",
          "marginType": "isolated",
          "isolatedMargin": "2.68573256",
          "isAutoAddMargin": "false",
          "positionSide": "BOTH",
          "notional": "-5.38164690",
          "isolatedWallet": "2.68857946",
          "updateTime": 1682279427514
       }
    ]

    - Для режима хедж-позиции:

    [
       {
          "symbol": "ADAUSDT",
          "positionAmt": "0",
          "entryPrice": "0.0",
          "markPrice": "0.38270000",
          "unRealizedProfit": "0.00000000",
          "liquidationPrice": "0",
          "leverage": "2",
          "maxNotionalValue": "30000000",
          "marginType": "isolated",
          "isolatedMargin": "0.00000000",
          "isAutoAddMargin": "false",
          "positionSide": "LONG",
          "notional": "0",
          "isolatedWallet": "0",
          "updateTime": 0
       },
       {
          "symbol": "ADAUSDT",
          "positionAmt": "-14",
          "entryPrice": "0.3823",
          "markPrice": "0.38270000",
          "unRealizedProfit": "-0.00560000",
          "liquidationPrice": "0.57054436",
          "leverage": "2",
          "maxNotionalValue": "30000000",
          "marginType": "isolated",
          "isolatedMargin": "2.66975912",
          "isAutoAddMargin": "false",
          "positionSide": "SHORT",
          "notional": "-5.35780000",
          "isolatedWallet": "2.67535912",
          "updateTime": 1682280093556
       }
    ]
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v2/positionRisk"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
        "symbol": symbol.upper(),
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

    get_current_position_symbol(symbol="ADAUSDT", time_stamp=str(round(time.time() * 1000)))
