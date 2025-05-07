import json
import random
import re
import time
from urllib.parse import urlparse

import tls_client
from random_user_agent.user_agent import UserAgent
from tls_client.response import Response

from configs import logger
from params import payload, basic_headers, client_identifier_list


class StockXParser:
    def __init__(self, products_url: str or list):
        self.products_url = [products_url] if isinstance(products_url, str) else products_url
        self.api_url = "https://stockx.com/api/p/e"
        self.payload = payload
        self.product_url = None

        # Create one session and spoof Chrome‑120 JA3 + HTTP/2
        self.session = self.new_session()

    def run(self):
        all_product_data = []
        # sleep_after = random.randint(2, 4)
        # counter = 1
        for product_url in self.products_url:
            time.sleep(random.randint(4, 7))
            self.product_url = product_url
            product_data = self.run_parser()
            logger.info(f"Product {product_data['product_name']} DATA: {product_data['data']}")
            all_product_data.append(product_data)
            # counter += 1
            # if sleep_after == counter:
            #   time.sleep(25, 30)
        return all_product_data

    def run_parser(self):
        # 1) GET the product page – sets stockx_session_id, maybe cf_clearance
        html_resp = self.session.get(self.product_url)
        # IF HTTP STATUS 403

        logger.info(f"STATUS CODE: {html_resp.status_code}")

        # If GET Request throws 403 status code - sleep, create new session and rerun the code.
        if html_resp.status_code == 403:
            logger.warning(f"HTTP 403 Forbidden for {self.product_url}")
            self.session = self.new_session()
            return self.run_parser()
        # 2) Grab every cookie the page set (including _pxhd, pxcts, _pxvid)
        cookies = self.session.cookies.get_dict()
        logger.info(f" Initial cookies: {cookies}")

        # 3) Extract size_map from __NEXT_DATA__
        size_map = self.invoke_size_data(html_resp)

        # 4) First attempt GraphQL
        data = self._post_api(basic_headers)

        # 5) If ABR, solve it in the same session
        if "hostUrl" in data:
            logger.info("ABR detected, solving challenge…")
            self.solve_captcha(data, basic_headers)
            # small jitter
            # time.sleep(random.uniform(1.0, 2.5))
            data = self._post_api(basic_headers)

        # 6) Combine size + price
        variants = data["data"]["product"]["variants"]
        product_data = {}
        result = []
        for v in variants:
            vid = v["id"]
            size = size_map.get(vid, "UNKNOWN")
            price = v.get("market").get("state").get("lowestAsk")
            if type(price) is dict and price:
                price = price["amount"]
            result.append({"size": size, "price": price})
        product_data["product_name"] = data["data"]["product"]["title"]
        product_data["product_url"] = self.product_url
        product_data['data'] = result
        return product_data

    @staticmethod
    def invoke_size_data(html_resp: Response) -> dict:
        # pull Next.js blob
        m = re.search(
            r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
            html_resp.text, re.S
        )
        blob = json.loads(m.group(1))
        variants = \
            blob["props"]["pageProps"]["req"]["appContext"]["states"]["query"]["value"]["queries"][3]["state"][
                "data"][
                "product"]["variants"]

        # map id → size
        return {v["id"]: v["sizeChart"]["displayOptions"][0]['size'] for v in variants}

    def _post_api(self, headers):
        # update slug
        slug = urlparse(self.product_url).path.rstrip("/").split("/")[-1]
        self.payload["variables"]["id"] = slug

        # Add Apollo POST Request headers
        headers["apollographql-client-name"] = "Iron"
        headers["apollographql-client-version"] = "2025.04.20.00"
        headers["User-Agent"] = self.session.headers['User-Agent']
        resp = self.session.post(self.api_url, json=self.payload, headers=headers)

        # if 403, raise so we can retry after solve
        if resp.status_code == 403:
            logger.warning(f"Received 403 from API: {resp.text}")
            self.session = self.new_session()
            return self.run_parser()

        logger.info(f"API STATUS CODE: {resp.status_code}")
        return resp.json()

    def solve_captcha(self, data, headers):
        # Solve PerimeterX via hostUrl XHR in same session
        solve_body = {"appId": data["appId"], "uuid": data["uuid"], "vid": data["vid"]}
        # include same headers + cookies
        headers2 = headers.copy()
        headers2["Accept"] = "application/json"
        # call the XHR endpoint
        session = self.session  # same session
        session.post("https://stockx.com" + data["hostUrl"],
                     json=solve_body,
                     headers=headers2)

    def new_session(self):
        # Choose random client_identifier
        client_id = random.choice(client_identifier_list)

        # Create new session
        session = tls_client.Session(
            client_identifier=client_id,
            random_tls_extension_order=True,
        )

        # TODO: ADD PROXY
        # Get random user angent and add to session
        ua = UserAgent().get_random_user_agent()
        session.headers['User-Agent'] = ua
        session.headers.update({
            "sec-ch-ua": f"\"{ua.split('/')[0]}\";v=\"{ua.split(' ')[-1]}\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Origin": "https://stockx.com",
            "Referer": "https://stockx.com/"
        })
        logger.info(f"New session: client={client_id}")
        return session
