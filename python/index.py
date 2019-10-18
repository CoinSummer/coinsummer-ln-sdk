import functools
import hashlib
import hmac
import json
import random
import time
import binascii
from binascii import b2a_hex, a2b_hex
from cmd import Cmd

try:
    from urllib.parse import urlencode
except Exception:
    from urllib import urlencode

from pycoin.key import Key

from pycoin.encoding import from_bytes_32

import requests

COBO_PUB = "032f45930f652d72e0c90f71869dfe9af7d713b1f67dc2f7cb51f9572778b9c876"
FAKE_INNER_SECRET = "FAKE_SECRET"
API_HOST = "http://localhost:3000"

def double_hash256(content):
    return hashlib.sha256(hashlib.sha256(content.encode()).digest()).digest()


def verify(content, signature, pub_key):
    key = Key.from_sec(a2b_hex(pub_key))
    return key.verify(double_hash256(content), a2b_hex(signature))


def generate_ecc_signature(content, appSecret):
    # keyStr = Key(secret_exponent=from_bytes_32(a2b_hex(key)))
    # print(keyStr)
    # return b2a_hex(keyStr.sign(double_hash256(content))).decode()
    # test = binascii.hexlify(appSecret.encode())
    # keys = Key(secret_exponent=from_bytes_32(a2b_hex(appSecret.encode())))
    bin_key = bin(int(binascii.hexlify(appSecret.encode()), 16))
    private_key = binascii.a2b_hex(bin_key)
    print(private_key)
    test = from_bytes_32(private_key)
    # keyStr = Key(secret_exponent=from_bytes_32(private_key))
    print(test)
    keys = Key(secret_exponent=test)
    print(keys)
    return ''


def generate_hmac_signature(content, key):
    return hmac.new(key.encode(), content.encode(), hashlib.sha256).hexdigest()


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
        success = verify("%s|%s" % (content, timestamp), signature, COBO_PUB)
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
        resp = requests.post("%s%s" % (host, path), data=params, headers=headers)
    else:
        raise Exception("Not support http method")
    verify_success, result = verify_response(resp)
    if not verify_success:
        raise Exception("Fatal: verify content error, maybe encounter mid man attack")
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
        res = method(url, data, self.key, self.secret, self.host, self.sign_type)
        print(json.dumps(res, indent=4))

    def create_payment(self, amount, expiry):
        return self._request(
            post, "/v1/payment/", {"amount": amount, "expiry": expiry}
        )

    def get_payment(self, paymentId):
        return self._request(get, "/v1/payment/" + paymentId, {})

if __name__ == "__main__":
    # Replace by your own keys
    app_key = "HO21KDWFW8TC"
    api_secret = "1N5JOH9SU64Q1217EWJIIGI5PW214ZNL"
    api_host = API_HOST
    client = Client(
        app_key=app_key,
        api_secret=api_secret,
        host=api_host,
        sign_type="ecdsa",
    )
    client.create_payment(1024, 1800)
    print(client)
    # client.cmdloop()
