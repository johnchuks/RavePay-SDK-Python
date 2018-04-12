import requests
import os
import json
from dotenv import find_dotenv, load_dotenv
from ravepaypysdk.utils.encryption import encrypt_data
from ravepaypysdk.api import Api
from ravepaypysdk.resources import PreAuthorization, ValidateCharge, Transaction, Bank, Payment, PaymentPlan

load_dotenv(find_dotenv())

url = "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/charge"

client_payload = {
    "cardno": "5438898014560229",
    "cvv": "789",
    "is_mobile_money_gh": "1",
    "payment-type": "mobilemoneygh",
    "expirymonth": "07",
    "expiryyear": "18",
    "currency": "GHS",
    "pin": "7552",
    "country": "GH",
    "amount": "10",
    "network": "MTN",
    "email": "user@example.com",
    "phonenumber": "1234555",
    "suggested_auth": "PIN",
    "firstname": "user1",
    "lastname": "user2",
    "IP": "355426087298442",
    "txRef": "MC-7663-YU",
    "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
}

account_payload = {
    "accountnumber": "0690000004",
    "accountbank": "044",
    "currency": "NGN",
    "country": "NG",
    "amount": "10",
    "email": "user@example.com",
    "phonenumber": "1234555",
    "firstname": "first name",
    "lastname": "last name",
    "IP": "355426087298442",
    "txRef": "",
    "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
}

encrypted_payload = encrypt_data(os.environ.get('secret_key'), json.dumps(client_payload))

payload = dict(PBFPubKey=os.environ.get('public_key'), client=encrypted_payload, alg='3DES-24')
# validate_payload = dict(transaction_reference='FLW-MOCK-bad59ea46faf0f0e9935826893c3070b', otp='12345')
#
new_api = Api(secret_key=os.environ.get('secret_key'),
              public_key=os.environ.get('public_key'),
                            production=False)

single_payload = {
    "amount": 3000,
    "name": 'bosco pan',
    "intervals": "daily",
    "duration": 0
}
params = {
   'id': 70,
}
cancel_payment = PaymentPlan.edit_plan(plan_id=71, api=new_api)
print(cancel_payment, '------->>>>')
