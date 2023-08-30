import requests
import json


def get_symbols_info() -> dict:

    """
    Запрос:
    Получить текущие правила биржевой торговли и информацию о символах

    Полный url:
    "https://fapi.binance.com/fapi/v1/exchangeInfo"

    Вес запроса:
    1

    Параметры:
    - None

    Комментарии:
    - None

    Ответ:
    {
        "exchangeFilters": [],
        "rateLimits": [
            {
                "interval": "MINUTE",
                "intervalNum": 1,
                "limit": 2400,
                "rateLimitType": "REQUEST_WEIGHT"
            },
            {
                "interval": "MINUTE",
                "intervalNum": 1,
                "limit": 1200,
                "rateLimitType": "ORDERS"
            }
        ],
        "serverTime": 1565613908500,  (ignore)
        "assets": [ (информация об активах)
            {
                "asset": "BUSD",
                "marginAvailable": true,  (можно ли использовать актив в качестве маржи в режиме Multi-Assets)
                "autoAssetExchange": 0  (порог автоматического обмена в режиме маржи Multi-Assets)
            },
            {
                "asset": "USDT",
                "marginAvailable": true,
                "autoAssetExchange": 0
            },
            {
                "asset": "BNB",
                "marginAvailable": false,
                "autoAssetExchange": null
            }
        ],
        "symbols": [
            {
                "symbol": "BLZUSDT",
                "pair": "BLZUSDT",
                "contractType": "PERPETUAL",
                "deliveryDate": 4133404800000,
                "onboardDate": 1598252400000,
                "status": "TRADING",
                "maintMarginPercent": "2.5000",  (ignore)
                "requiredMarginPercent": "5.0000",  (ignore)
                "baseAsset": "BLZ",
                "quoteAsset": "USDT",
                "marginAsset": "USDT",
                "pricePrecision": 5,  (пожалуйста, не используйте его как tickSize)
                "quantityPrecision": 0,  (пожалуйста, не используйте его как stepSize)
                "baseAssetPrecision": 8,
                "quotePrecision": 8,
                "underlyingType": "COIN",
                "underlyingSubType": ["STORAGE"],
                "settlePlan": 0,
                "triggerProtect": "0.15",  (порог для алгоритмического заказа с "priceProtect")
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "maxPrice": "300",
                        "minPrice": "0.0001",
                        "tickSize": "0.0001"
                    },
                    {
                        "filterType": "LOT_SIZE",
                        "maxQty": "10000000",
                        "minQty": "1",
                        "stepSize": "1"
                    },
                    {
                        "filterType": "MARKET_LOT_SIZE",
                        "maxQty": "590119",
                        "minQty": "1",
                        "stepSize": "1"
                    },
                    {
                        "filterType": "MAX_NUM_ORDERS",
                        "limit": 200
                    },
                    {
                        "filterType": "MAX_NUM_ALGO_ORDERS",
                        "limit": 100
                    },
                    {
                        "filterType": "MIN_NOTIONAL",
                        "notional": "5.0",
                    },
                    {
                        "filterType": "PERCENT_PRICE",
                        "multiplierUp": "1.1500",
                        "multiplierDown": "0.8500",
                        "multiplierDecimal": 4
                    }
                ],
                "OrderType": [
                    "LIMIT",
                    "MARKET",
                    "STOP",
                    "STOP_MARKET",
                    "TAKE_PROFIT",
                    "TAKE_PROFIT_MARKET",
                    "TRAILING_STOP_MARKET"
                ],
                "timeInForce": [
                    "GTC",
                    "IOC",
                    "FOK",
                    "GTX"
                ],
                "liquidationFee": "0.010000",  (ставка ликвидационного сбора)
                "marketTakeBound": "0.30",  (максимальная разница в цене (от цены маркировки), которую может сделать рыночный ордер)
            }
        ],
        "timezone": "UTC"
    }
    """

    # ------------------------------------------
    base_url = "https://fapi.binance.com"
    end_point = "/fapi/v1/exchangeInfo"
    # ------------------------------------------

    complete_request = base_url + end_point

    response = requests.get(url=complete_request)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "headers": response.headers, "result": result}
    else:
        return {"status_code": response.status_code, "headers": response.headers, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    result_2 = get_symbols_info()

    if result_2["status_code"] == 200:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("result:", result_2["result"])
    else:
        print("status_code:", result_2["status_code"])
        print("headers:", result_2["headers"])
        print("code_error:", result_2["code_error"])
        print("text_error:", result_2["text_error"])
