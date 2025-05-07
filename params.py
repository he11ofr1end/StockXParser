

payload = {
    "query": "query GetMarketData("
             "$id: String!, "
             "$currencyCode: CurrencyCode, "
             "$countryCode: String!, "
             "$marketName: String, "
             "$viewerContext: MarketViewerContext) "
             "{\n  product(id: $id) "
             "{\n    id\n    urlKey\n    listingType\n    title\n    uuid\n    contentGroup\n    "
             "sizeDescriptor\n    productCategory\n    lockBuying\n    lockSelling\n    "
             "media {\n      imageUrl\n    }\n    minimumBid(currencyCode: $currencyCode)\n    "
             "market(currencyCode: $currencyCode) "
             "{\n      state(country: $countryCode, market: $marketName) "
             "{\n        lowestAsk {\n          amount\n          chainId\n        }\n        "
             "highestBid {\n          amount\n        }\n        askServiceLevels {\n          expressExpedited {\n   "
             "         count\n            lowest {\n              amount\n              chainId\n              "
             "inventoryType\n            }\n            delivery {\n              expectedDeliveryDate\n              "
             "latestDeliveryDate\n            }\n          }\n          expressStandard {\n            count\n        "
             "    lowest {\n              amount\n              inventoryType\n            }\n            delivery {"
             "\n              expectedDeliveryDate\n              latestDeliveryDate\n            }\n          }\n    "
             "      standard {\n            count\n            lowest {\n              amount\n              "
             "chainId\n            }\n          }\n        }\n        numberOfAsks\n        numberOfBids\n      }\n   "
             "   salesInformation {\n        lastSale\n        salesLast72Hours\n      }\n      statistics(market: "
             "$marketName, viewerContext: $viewerContext) {\n        lastSale {\n          amount\n          "
             "changePercentage\n          changeValue\n          sameFees\n        }\n      }\n    }\n    variants {"
             "\n      id\n      market(currencyCode: $currencyCode) {\n        state(country: $countryCode, "
             "market: $marketName) {\n          lowestAsk {\n            amount\n            chainId\n          }\n   "
             "       highestBid {\n            amount\n          }\n          askServiceLevels {\n            "
             "expressExpedited {\n              count\n              lowest {\n                amount\n               "
             " chainId\n                inventoryType\n              }\n              delivery {\n                "
             "expectedDeliveryDate\n                latestDeliveryDate\n              }\n            }\n            "
             "expressStandard {\n              count\n              lowest {\n                amount\n                "
             "chainId\n                inventoryType\n              }\n              delivery {\n                "
             "expectedDeliveryDate\n                latestDeliveryDate\n              }\n            }\n            "
             "standard {\n              count\n              lowest {\n                amount\n                "
             "chainId\n              }\n            }\n          }\n          numberOfAsks\n          numberOfBids\n  "
             "      }\n        salesInformation {\n          lastSale\n          salesLast72Hours\n        }\n        "
             "statistics(market: $marketName, viewerContext: $viewerContext) {\n          lastSale {\n            "
             "amount\n            changePercentage\n            changeValue\n            sameFees\n          }\n      "
             "  }\n      }\n    }\n  }\n}",
    "variables": {
        "id": "",
        "currencyCode": "USD",
        "countryCode": "AM",
        "marketName": "AM",
        "viewerContext": "BUYER"
    },
    "operationName": "GetMarketData"
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "apollographql-client-name": "Iron",
    "apollographql-client-version": "2025.04.20.00",
}

basic_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    # fingerprint headers to mimic real browser XHR
    # "sec-ch-ua": "\"Chromium\";v=\"120\", \"Not A;Brand\";v=\"99\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "User-Agent": "",
    "Origin": "https://stockx.com",
    "Referer": "https://stockx.com/"
}

client_identifier_list = ['chrome_103', 'chrome_104', 'chrome_105', 'chrome_106', 'chrome_107', 'chrome_108',
                          'chrome109', 'Chrome110', 'chrome111', 'chrome112', 'chrome_116_PSK', 'chrome_116_PSK_PQ',
                          'chrome_117', 'chrome_120', 'safari_ios_15_5', 'safari_ios_15_6', 'safari_ios_16_0',
                          'firefox_102', 'firefox_104', 'firefox108', 'Firefox110', 'firefox_117', 'firefox_120']
