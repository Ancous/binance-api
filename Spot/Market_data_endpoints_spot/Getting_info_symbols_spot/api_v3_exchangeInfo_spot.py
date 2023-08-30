import requests
import json

from urllib.parse import urlencode


def get_symbols_info_spot(list_symbols: list = None) -> dict:

    """
    Запрос:
    Получить текущие правила биржевой торговли и информацию о символах для спота

    Полный url:
    "https://api.binance.com/api/v3/exchangeInfo"

    Вес запроса:
    10

    Параметры:
    - list_symbols="symbols" (list): актив (["BTCUSDT"], ["BTCUSDT", "ADAUSDT"], ...)

    Комментарии:
    - None

    Ответ:
    {
       "timezone": "UTC",
       "serverTime": 1686560333688,
       "rateLimits": [
          {
             "rateLimitType": "REQUEST_WEIGHT",
             "interval": "MINUTE",
             "intervalNum": 1,
             "limit": 1200
          },
          {
             "rateLimitType": "ORDERS",
             "interval": "SECOND",
             "intervalNum": 10,
             "limit": 50
          },
          {
             "rateLimitType": "ORDERS",
             "interval": "DAY",
             "intervalNum": 1,
             "limit": 160000
          },
          {
             "rateLimitType": "RAW_REQUESTS",
             "interval": "MINUTE",
             "intervalNum": 5,
             "limit": 6100
          }
       ],
       "exchangeFilters": [],
       "symbols": [
          {
             "symbol": "ADAUSDT",
             "status": "TRADING",
             "baseAsset": "ADA",
             "baseAssetPrecision": 8,
             "quoteAsset": "USDT",
             "quotePrecision": 8,
             "quoteAssetPrecision": 8,
             "baseCommissionPrecision": 8,
             "quoteCommissionPrecision": 8,
             "orderTypes": [
                "LIMIT",
                "LIMIT_MAKER",
                "MARKET",
                "STOP_LOSS_LIMIT",
                "TAKE_PROFIT_LIMIT"
             ],
             "icebergAllowed": true,
             "ocoAllowed": true,
             "quoteOrderQtyMarketAllowed": true,
             "allowTrailingStop": true,
             "cancelReplaceAllowed": true,
             "isSpotTradingAllowed": true,
             "isMarginTradingAllowed": true,
             "filters": [
                {
                   "filterType": "PRICE_FILTER",
                   "minPrice": "0.00010000",
                   "maxPrice": "1000.00000000",
                   "tickSize": "0.00010000"
                },
                {
                   "filterType": "LOT_SIZE",
                   "minQty": "0.10000000",
                   "maxQty": "900000.00000000",
                   "stepSize": "0.10000000"
                },
                {
                   "filterType": "ICEBERG_PARTS",
                   "limit": 10
                },
                {
                   "filterType": "MARKET_LOT_SIZE",
                   "minQty": "0.00000000",
                   "maxQty": "2723864.64079221",
                   "stepSize": "0.00000000"
                },
                {
                   "filterType": "TRAILING_DELTA",
                   "minTrailingAboveDelta": 10,
                   "maxTrailingAboveDelta": 2000,
                   "minTrailingBelowDelta": 10,
                   "maxTrailingBelowDelta": 2000
                },
                {
                   "filterType": "PERCENT_PRICE_BY_SIDE",
                   "bidMultiplierUp": "5",
                   "bidMultiplierDown": "0.2",
                   "askMultiplierUp": "5",
                   "askMultiplierDown": "0.2",
                   "avgPriceMins": 5
                },
                {
                   "filterType": "NOTIONAL",
                   "minNotional": "5.00000000",
                   "applyMinToMarket": true,
                   "maxNotional": "9000000.00000000",
                   "applyMaxToMarket": false,
                   "avgPriceMins": 5
                },
                {
                   "filterType": "MAX_NUM_ORDERS",
                   "maxNumOrders": 200
                },
                {
                   "filterType": "MAX_NUM_ALGO_ORDERS",
                   "maxNumAlgoOrders": 5
                }
             ],
             "permissions": [
                "SPOT",
                "MARGIN",
                "TRD_GRP_005",
                "TRD_GRP_006"
             ],
             "defaultSelfTradePreventionMode": "NONE",
             "allowedSelfTradePreventionModes": [
                "NONE",
                "EXPIRE_TAKER",
                "EXPIRE_MAKER",
                "EXPIRE_BOTH"
             ]
          }
       ]
    }
    """

    # ------------------------------------------
    base_url = "https://api.binance.com"
    end_point = "/api/v3/exchangeInfo"
    if list_symbols:
        parameters = {
                "symbols": [symbol.upper() for symbol in list_symbols]
            }
    else:
        parameters = {}
    # ------------------------------------------

    complete_request = base_url + end_point
    complete_parameters = urlencode(parameters).replace('%2C+', ',').replace('%27', '%22')

    response = requests.get(url=complete_request, params=complete_parameters)
    result = json.loads(response.text)

    if response.status_code == 200:
        with open("answer.json", "w") as file:
            json.dump(obj=result, fp=file, indent=3)
        return {"status_code": response.status_code, "result": result}
    else:
        return {"status_code": response.status_code, "code_error": result['code'], "text_error": result['msg']}


if __name__ in "__main__":

    get_symbols_info_spot(list_symbols=["ADAUSDT", "ETHUSDT"])
