import requests
import time
import json
import os
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()


def get_info_account(time_stamp: str,
                     recv_window: str = "5000") -> dict:
  
    """
    Запрос:
    Получить текущую информацию об учетной записи

    Полный url:
    "https://fapi.binance.com/fapi/v2/account"

    Вес запроса:
    5

    Параметры:
    - time_stamp="timestamp" (str): время отправки запроса ("1681501516492", ...)
    - recv_window="recvWindow" (str): количество миллисекунд, в течение которых запрос действителен ("1000", ..., "70000")

    Комментарии:
    - None

    Ответ:
    - режим single-asset

    {
        "feeTier": 0,   (уровень комиссии счета)
        "canTrade": true,   ("true" если можно торговать, "false" нельзя торговать)
        "canDeposit": true,   ("true" если можно перевести актив, "false" нельзя перевести актив)
        "canWithdraw": true,   ("true" если можно вывести актив, "false" нельзя вывести актив)
        "updateTime": 0,   (ignore)
        "multiAssetsMargin": false,
        "totalInitialMargin": "0.00000000",   (необходимая начальная маржа с текущей ценой маркировки (бесполезно с изолированными позициями), только для актива USDT)
        "totalMaintMargin": "0.00000000",   (необходимая поддерживающая маржа, только для актива USDT)
        "totalWalletBalance": "23.72469206",   (баланс кошелька, только для актива USDT)
        "totalUnrealizedProfit": "0.00000000",   (нереализованная прибыль, только для актива USDT)
        "totalMarginBalance": "23.72469206",   (баланс маржи, только для актива USDT)
        "totalPositionInitialMargin": "0.00000000",   (начальная маржа необходимая для позиций с текущей ценой маркировки, только для актива USDT)
        "totalOpenOrderInitialMargin": "0.00000000",   (начальная маржа, необходимая для открытых ордеров с текущей ценой маркировки, только для актива USDT)
        "totalCrossWalletBalance": "23.72469206",   (перекрёстный баланс кошелька, только для актива USDT)
        "totalCrossUnPnl": "0.00000000",   (нереализованная прибыль по пересеченным позициям, только для актива USDT)
        "availableBalance": "23.72469206",   (доступный баланс, только для актива USDT)
        "maxWithdrawAmount": "23.72469206"   (максимальная сумма для вывода, только для актива USDT)
        "assets": [
            {
                "asset": "USDT",   (название актива)
                "walletBalance": "23.72469206",   (баланс кошелька)
                "unrealizedProfit": "0.00000000",   (нереализованная прибыль)
                "marginBalance": "23.72469206",   (баланс маржи)
                "maintMargin": "0.00000000",   (необходимая поддерживающая маржа)
                "initialMargin": "0.00000000",   (необходимая начальная маржа с текущей ценой маркировки)
                "positionInitialMargin": "0.00000000",   (начальная маржа, необходимая для позиций с текущей ценой маркировки)
                "openOrderInitialMargin": "0.00000000",   (начальная маржа, необходимая для открытых ордеров с текущей ценой маркировки)
                "crossWalletBalance": "23.72469206",   (сокращённый баланс кошелька)
                "crossUnPnl": "0.00000000"   (нереализованная прибыль пересеченных позиций)
                "availableBalance": "23.72469206",   (доступный баланс)
                "maxWithdrawAmount": "23.72469206",   (максимальная сумма для вывода)
                "marginAvailable": true,      ("true" можно использовать актив в качестве маржи в режиме Multi-Assets, "false" нельзя использовать актив в качестве маржи в режиме Multi-Assets)
                "updateTime": 1625474304765   (время последнего обновления)
            },
            {
                "asset": "BUSD",   (название актива)
                "walletBalance": "103.12345678",   (баланс кошелька)
                "unrealizedProfit": "0.00000000",   (нереализованная прибыль)
                "marginBalance": "103.12345678",   (баланс маржи)
                "maintMargin": "0.00000000",   (maintenance margin required)
                "initialMargin": "0.00000000",   (необходимая начальная маржа с текущей ценой маркировки)
                "positionInitialMargin": "0.00000000",   (начальная маржа, необходимая для позиций с текущей ценой маркировки)
                "openOrderInitialMargin": "0.00000000",   (начальная маржа, необходимая для открытых ордеров с текущей ценой маркировки)
                "crossWalletBalance": "103.12345678",   (сокращённый баланс кошелька)
                "crossUnPnl": "0.00000000"   (нереализованная прибыль пересеченных позиций)
                "availableBalance": "103.12345678",   (доступный баланс)
                "maxWithdrawAmount": "103.12345678",   (максимальная сумма для вывода)
                "marginAvailable": true,   ("true" можно использовать актив в качестве маржи в режиме Multi-Assets, "false" нельзя использовать актив в качестве маржи в режиме Multi-Assets)
                "updateTime": 1625474304765   (время последнего обновления)
            }
        ],
        "positions": [   (возвращаются позиции всех символов на рынке. В одностороннем режиме будут возвращены только "BOTH" позиции. В режиме хеджирования будут возвращены только "LONG" и "SHORT" позиции)
            {
                "symbol": "BTCUSDT",  (название символа)
                "initialMargin": "0",  (необходимая начальная маржа с текущей ценой маркировки)
                "maintMargin": "0",  (необходимая поддерживающая маржа)
                "unrealizedProfit": "0.00000000",  (нереализованная прибыль)
                "positionInitialMargin": "0",  (начальная маржа, необходимая для позиций с текущей ценой маркировки)
                "openOrderInitialMargin": "0",  (начальная маржа, необходимая для открытых ордеров с текущей ценой маркировки)
                "leverage": "100",  (текущее начальное плечо)
                "isolated": true,  ("true" если позиция изолирована)
                "entryPrice": "0.00000",  (средняя цена входа)
                "maxNotional": "250000",  (максимально доступный номинал с текущим кредитным плечом)
                "bidNotional": "0",  (ignore)
                "askNotional": "0",  (ignore)
                "positionSide": "BOTH",  (сторона позиции)
                "positionAmt": "0",  (сумма позиции)
                "updateTime": 0  (время последнего обновления)
            }
        ]
    }

    - Режим multi-assets

    {
        "feeTier": 0,  (уровень комиссии счета)
        "canTrade": true,  ("true" если можно торговать, "false" нельзя торговать)
        "canDeposit": true,  ("true" если можно перевести актив, "false" нельзя перевести актив)
        "canWithdraw": true,  ("true" если можно вывести актив, "false" нельзя вывести актив)
        "updateTime": 0,  (ignore)
        "multiAssetsMargin": true,
        "totalInitialMargin": "0.00000000",  (сумма стоимости всех кросс-позиций/начальной маржи открытого ордера в долларах США)
        "totalMaintMargin": "0.00000000",  (сумма долларовой стоимости всех кросс-позиций, поддерживающих маржу)
        "totalWalletBalance": "126.72469206",  (баланс кошелька в долларах США)
        "totalUnrealizedProfit": "0.00000000",  (нереализованная прибыль в долларах США)
        "totalMarginBalance": "126.72469206",  (баланс маржи в долларах США)
        "totalPositionInitialMargin": "0.00000000",  (сумма стоимости начальной маржи всех кросс-позиций в долларах США)
        "totalOpenOrderInitialMargin": "0.00000000",  (необходимая начальная маржа для открытых ордеров с текущей ценой маркировки в долларах США)
        "totalCrossWalletBalance": "126.72469206",  (баланс кошелька в долларах США)
        "totalCrossUnPnl": "0.00000000",  (нереализованная прибыль пересеченных позиций в долларах США)
        "availableBalance": "126.72469206",  (доступный баланс в долларах США)
        "maxWithdrawAmount": "126.72469206"  (доступный баланс в долларах США)
        "assets": [
            {
                "asset": "USDT",  (название актива)
                "walletBalance": "23.72469206",  (баланс кошелька)
                "unrealizedProfit": "0.00000000",  (нереализованная прибыль)
                "marginBalance": "23.72469206",  (баланс маржи)
                "maintMargin": "0.00000000",  (необходимая поддерживающая маржа)
                "initialMargin": "0.00000000",  (необходимая начальная маржа с текущей ценой маркировки)
                "positionInitialMargin": "0.00000000",  (начальная маржа, необходимая для позиций с текущей ценой маркировки)
                "openOrderInitialMargin": "0.00000000",  (начальная маржа, необходимая для открытых ордеров с текущей ценой маркировки)
                "crossWalletBalance": "23.72469206",  (сокращённый баланс кошелька)
                "crossUnPnl": "0.00000000",  (нереализованная прибыль пересеченных позиций)
                "availableBalance": "23.72469206",  (доступный баланс)
                "maxWithdrawAmount": "23.72469206",  (максимальная сумма для вывода)
                "marginAvailable": true,  (("true" можно использовать актив в качестве маржи в режиме Multi-Assets, "false" нельзя использовать актив в качестве маржи в режиме Multi-Assets))
                "updateTime": 1625474304765  (время последнего обновления)
            },
            {
                "asset": "BUSD",  (название актива)
                "walletBalance": "103.12345678",  (баланс кошелька)
                "unrealizedProfit": "0.00000000",  (нереализованная прибыль)
                "marginBalance": "103.12345678",  (баланс маржи)
                "maintMargin": "0.00000000",  (необходимая поддерживающая маржа)
                "initialMargin": "0.00000000",  (необходимая начальная маржа с текущей ценой маркировки)
                "positionInitialMargin": "0.00000000",  (начальная маржа, необходимая для позиций с текущей ценой маркировки)
                "openOrderInitialMargin": "0.00000000",  (начальная маржа, необходимая для открытых ордеров с текущей ценой маркировки)
                "crossWalletBalance": "103.12345678",  (сокращённый баланс кошелька)
                "crossUnPnl": "0.00000000",  (нереализованная прибыль пересеченных позиций)
                "availableBalance": "103.12345678",  (доступный баланс)
                "maxWithdrawAmount": "103.12345678",  (максимальная сумма для вывода)
                "marginAvailable": true,  (("true" можно использовать актив в качестве маржи в режиме Multi-Assets, "false" нельзя использовать актив в качестве маржи в режиме Multi-Assets))
                "updateTime": 1625474304765  (время последнего обновления)
            }
        ],
        "positions": [   (возвращаются позиции всех символов на рынке. В одностороннем режиме будут возвращены только "BOTH" позиции. В режиме хеджирования будут возвращены только "LONG" и "SHORT" позиции)

            {
                "symbol": "BTCUSDT",  (название символа)
                "initialMargin": "0",  (необходимая начальная маржа с текущей ценой маркировки)
                "maintMargin": "0",  (необходимая поддерживающая маржа)
                "unrealizedProfit": "0.00000000",  (нереализованная прибыль)
                "positionInitialMargin": "0",  (начальная маржа, необходимая для позиций с текущей ценой маркировки)
                "openOrderInitialMargin": "0",  (начальная маржа, необходимая для открытых ордеров с текущей ценой маркировки)
                "leverage": "100",  (текущее начальное плечо)
                "isolated": true,  ("true" если позиция изолирована)
                "entryPrice": "0.00000",  (средняя цена входа)
                "maxNotional": "250000",  (максимально доступный номинал с текущим кредитным плечом)
                "bidNotional": "0",  (ignore)
                "askNotional": "0",  (ignore)
                "positionSide": "BOTH",  (сторона позиции)
                "positionAmt": "0",  (сумма позиции)
                "updateTime": 0  (время последнего обновления)
            }
        ]
    }
    """

    # -------------------------------------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v2/account"
    api_key = os.getenv("api_key")
    secret_key = os.getenv("secret_key")
    parameters = {
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
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_info_account(time_stamp=str(round(time.time() * 1000)))

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
