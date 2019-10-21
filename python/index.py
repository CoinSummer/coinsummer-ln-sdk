from binascii import hexlify, unhexlify
import functools
import hashlib
import hmac
import json
import random
import time
import binascii
from binascii import b2a_hex, a2b_hex
from ecdsa import SigningKey, SECP256k1

try:
    from urllib.parse import urlencode
except Exception:
    from urllib import urlencode

from pycoin.key import Key

from pycoin.encoding import from_bytes_32

import requests

RAZZIL_PUB = "032f45930f652d72e0c90f71869dfe9af7d713b1f67dc2f7cb51f9572778b9c876"
API_HOST = "http://razzil-api.dev.csiodev.com"
APP_KEY = "W4R4IHQNBB91PG6K"
APP_SECRET = "016f47e0bcf9a152dd216d1990468c1cb9aa29e82bf2bbc303e15c597add404b"


def double_hash256(content):
    return hashlib.sha256(hashlib.sha256(content.encode()).digest()).digest()


def verify(content, signature, pub_key):
    key = Key.from_sec(a2b_hex(pub_key))
    return key.verify(double_hash256(content), a2b_hex(signature))


def generate_ecc_signature(content, key):
    key = Key(secret_exponent=from_bytes_32(a2b_hex(key)))
    return b2a_hex(key.sign(double_hash256(content))).decode()


def generate_hmac_signature(content, key):
    return hmac.new(key.encode(), content.encode(), hashlib.sha256).hexdigest()


def generate_private_secret(key):
    s = hashlib.sha256(bytes(key, 'utf-8')).digest()
    return hexlify(s).decode('ascii')


def sort_params(params):
    params = [(key, val) for key, val in params.items()]

    params.sort(key=lambda x: x[0])
    return urlencode(params)


def verify_response(response):
    content = response.content.decode()
    success = True
    try:
        timestamp = response.headers["BIZ_TIMESTAMP"]
        signature = response.headers["BIZ_RESP_SIGNATURE"]
        success = verify("%s|%s" % (content, timestamp), signature, RAZZIL_PUB)
    except KeyError:
        pass
    return success, json.loads(content)


def request(
    method,
    path,
    params,
    app_key,
    api_secret,
    host=API_HOST,
    sign_type="hmac",
):
    method = method.upper()
    nonce = str(int(time.time() * 1000))
    content = "%s|%s|%s|%s" % (method, path, nonce, sort_params(params))

    if sign_type == "hmac":
        sign = generate_hmac_signature(content, api_secret)
    else:
        sign = generate_ecc_signature(content, api_secret)

    headers = {
        "Biz-App-Key": app_key,
        "Biz-Api-Nonce": nonce,
        "Biz-Api-Signature": sign,
    }
    if method == "GET":
        resp = requests.get(
            "%s%s" % (host, path), params=urlencode(params), headers=headers
        )
    elif method == "POST":
        resp = requests.post("%s%s" % (host, path),
                             data=params, headers=headers)
    else:
        raise Exception("Not support http method")
    verify_success, result = verify_response(resp)
    if not verify_success:
        raise Exception(
            "Fatal: verify content error, maybe encounter mid man attack")
    return result


get = functools.partial(request, "GET")
post = functools.partial(request, "POST")


class Client():

    def __init__(
        self,
        app_key=None,
        api_secret=None,
        host=API_HOST,
        sign_type="hmac",
    ):
        super(Client, self).__init__()
        assert app_key
        assert api_secret
        assert sign_type in ("hmac", "ecdsa")
        self.key = app_key
        self.secret = api_secret
        self.host = host
        self.sign_type = sign_type

    def _request(self, method, url, data):
        res = method(url, data, self.key, self.secret,
                     self.host, self.sign_type)
        print(json.dumps(res, indent=4))

    def create_payment(self, amount, expiry):
        return self._request(
            post, "/v1/payment/", {"amount": amount, "expiry": expiry}
        )

    def get_payment(self, paymentId):
        return self._request(get, "/v1/payment/" + paymentId, {})


if __name__ == "__main__":
    # Replace by your own keys
    app_key = APP_KEY
    api_secret = APP_SECRET
    api_host = API_HOST
    client = Client(
        app_key=app_key,
        api_secret=api_secret,
        host=api_host,
        sign_type="ecdsa",
    )
    client.create_payment(1024, 1800)

    # 获取交易详情
    # client.get_payment('483fe08b-b5e8-4edc-8ff7-b8b7e7bb3bda')
