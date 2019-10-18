import functools
import hashlib
import hmac
import json
import random
import time
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
    host="http://localhost:3000",
    sign_type="hmac",
):
    method = method.upper()
    nonce = str(int(time.time() * 1000))
    content = "%s|%s|%s|%s" % (method, path, nonce, sort_params(params))
    if sign_type == "hmac":
        sign = generate_hmac_signature(content, api_secret)
    else:
        sign = generate_ecc_signature(content, api_secret)
    print(sign)

    # headers = {
    #     "Biz-App-Key": app_key,
    #     "Biz-Api-Nonce": nonce,
    #     "Biz-Api-Signature": sign,
    # }
    # if method == "GET":
    #     resp = requests.get(
    #         "%s%s" % (host, path), params=urlencode(params), headers=headers
    #     )
    # elif method == "POST":
    #     resp = requests.post("%s%s" % (host, path), data=params, headers=headers)
    # else:
    #     raise Exception("Not support http method")
    # verify_success, result = verify_response(resp)
    # if not verify_success:
    #     raise Exception("Fatal: verify content error, maybe encounter mid man attack")
    # return result


get = functools.partial(request, "GET")
post = functools.partial(request, "POST")


class Client(Cmd):
    prompt = "Razzil> "
    intro = "Welcome to the Razzil shell. Type help or ? to list commands. \n"

    def __init__(
        self,
        app_key=None,
        api_secret=None,
        host="http://localhost:3000",
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

    def do_create_payment(self, line):
        (
            "\n\tquery expiry if amount, format: \033[93m[amount] [expiry]\033[0m "
            "\n\texample: \033[91mquery_address LONT_ONT ADDRESS\033[0m\n"
        )
        if len(line.split()) != 2:
            print("format: [amount] [expiry]")
            return
        amount, expiry = line.split()
        return self._request(
            post, "/v1/payment/", {"amount": amount, "expiry": expiry}
        )

    def do_get_payment(self, line):
        (
            "\n\tshow detail of payment, format: \033[93m[paymentId]\033[0m "
            "\n\texample: \033[91mpayment LONT_ONT\033[0m\n"
        )
        paymentId = line.strip()
        return self._request(get, "/v1/payment/" + paymentId, {})


if __name__ == "__main__":
    # Replace by your own keys
    client = Client(
        app_key="HO21KDWFW8TC",
        api_secret="1N5JOH9SU64Q1217EWJIIGI5PW214ZNL",
        host="http://localhost:3000",
        sign_type="ecdsa",
    )

    client.cmdloop()
