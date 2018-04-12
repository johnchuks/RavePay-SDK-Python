import os
import unittest
from unittest.mock import patch
from dotenv import load_dotenv, find_dotenv
from ravepaypysdk.api import Api
from ravepaypysdk.resources import Transaction, Payment, Bank, PreAuthorization, ValidateCharge, PaymentPlan, Subscriptions

load_dotenv(find_dotenv())


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.new_api = Api(
            secret_key='dummy',
            public_key='dummy',
            production=False
        )
        self.payload = dict(error=False, Payment=1200, id=2)

    @patch('ravepaypysdk.resources.List.list')
    def test_single_recurring_transaction(self, mock):
        self.single_recurring_transac_payload = {
            "txId": 1
        }
        mc = mock.return_value
        mc.list.return_value = True
        result = Transaction.list_single_recurring(self.single_recurring_transac_payload, api=self.new_api)
        mock.assert_called_once_with('/merchant/subscriptions/list', self.new_api, {'seckey': 'dummy', 'txId': 1})
        self.assertTrue(result)

    @patch('ravepaypysdk.resources.List.list')
    def test_list_all_recurring_transaction(self, mock):
        mc = mock.return_value
        mc.list.return_value = True
        response = Transaction.list_all_recurring(api=self.new_api)
        mock.assert_called_once_with('/merchant/subscriptions/list', self.new_api, {'seckey': 'dummy'})
        self.assertTrue(response)

    @patch('ravepaypysdk.resources.Create.create')
    def test_refund(self, mock):
        mc = mock.return_value
        mc.list.return_value = True
        response = Transaction.refund(self.payload, api=self.new_api)
        mock.assert_called_once_with('/gpx/merchant/transactions/refund', self.new_api,
                                     {'error': False, 'Payment': 1200, 'id': 2, 'SECKEY': 'dummy'})
        self.assertTrue(response)

    @patch('ravepaypysdk.resources.Create.create')
    def test_stop_recurring_payment(self, mock):
        mc = mock.return_value
        mc.return_value = True
        response = Transaction.stop_recurring_payment(self.payload, api=self.new_api)
        mock.assert_called_once_with("/merchant/subscriptions/stop", self.new_api,
                                     {'seckey': 'dummy', 'error': False, 'Payment': 1200, 'id': 2})
        self.assertTrue(response)

    def test_stop_recurring_payment_exception(self):
        payload = dict(error=False, )
        self.assertRaises(KeyError, Transaction.stop_recurring_payment, payload, api=self.new_api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_verify_transaction(self, mock):
        path = '/flwv3-pug/getpaidx/api/verify'
        mc = mock.return_value
        mc.return_value = True
        verify_response = Transaction.verify(self.payload, api=self.new_api)
        mock.assert_called_once_with(path, self.new_api, {
            'error': False, 'Payment': 1200, 'id': 2, 'SECKEY': 'dummy'})
        self.assertTrue(verify_response)

    @patch('ravepaypysdk.resources.Create.create')
    def test_xquery_verify_transaction(self, mock):
        path = '/flwv3-pug/getpaidx/api/xrequery'
        xquery_response = Transaction.verify_query(self.payload, api=self.new_api)
        mock.assert_called_once_with(
            path, self.new_api, {
                'error': False, 'Payment': 1200, 'id': 2, 'SECKEY': 'dummy'}
        )
        self.assertTrue(xquery_response)


class TestPayment(unittest.TestCase):
    def setUp(self):
        self.new_api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )
        self.path = '/flwv3-pug/getpaidx/api/charge'
        self.card_payload = dict(error=False, cardno='34343', cvv='232', email='jb@gmail.com')
        self.bank_payload = dict(error=False, accountnumber='34343', accountbank='232')
        self.mpesa_payload = {
            'payment-type': 'mpesa',
            'is_mpesa': 1
        }
        self.gh_mobile_payload = {
            'payment-type': 'mobilemoneygh',
            'is_mobile_money_gh': 1
        }
        self.ussd_payload = {
            'payment_type': 'ussd',
            'is_ussd': 1
        }

    @patch('ravepaypysdk.resources.Create.create')
    def test_card_direct_payment(self, mock):
        Payment.card(self.card_payload, api=self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'Zah+qD4JviOdUFttZL7d0MgB/LPtEW4Gz7werMMDtOIWZLCGeZ7hRb0PlZbPU6JfELIgpyUP/L9ylb58B6EpXGPYHhYjC/Uza94nb4ZLiJM=',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    def test_card_payment_exception(self):
        self.assertRaises(KeyError, Payment.card, self.bank_payload, api=self.new_api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_bank_account_direct_payment(self, mock):
        Payment.bank_account(self.bank_payload, api=self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'Zah+qD4JviOdUFttZL7d0D1iXdxyTXxBCbWZvXCfmUrkhNr7MxySJLe/01oZZxph27HEjbbOZVJCsD+WMA8Cjj78w8CcOF0t',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    def test_bank_account_payment_exception(self):
        self.assertRaises(KeyError, Payment.bank_account, self.card_payload, api=self.new_api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_mpesa_direct_payment(self, mock):
        Payment.mpesa(self.mpesa_payload, self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'BX1KArxf7xAngqqNs/uWpMcxilwH0CmJ0pMwxLLFPtXClSO3y4oSqD78w8CcOF0t',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    def test_mpesa_payment_exception(self):
        self.assertRaises(KeyError, Payment.mpesa, self.card_payload, api=self.new_api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_gh_money_payment(self, mock):
        Payment.ghana_mobile(self.gh_mobile_payload, self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'BX1KArxf7xAngqqNs/uWpF1xwWg3A0stKlGYVIidO/hNNG86I+JiSE7q7FFVlKolnQv3RdAjAqQu0ZCzmKFRog==',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    def test_gh_money_payment_exception(self):
        self.assertRaises(KeyError, Payment.ghana_mobile, self.card_payload, api=self.new_api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_ussd_payment(self, mock):
        Payment.ussd(self.ussd_payload, self.new_api)
        mock.assert_called_once_with(self.path, self.new_api,
                                     {
                                         'client': b'BX1KArxf7xCQvJirHHQBNK1AAZ9qzlza9vNv8GjMkIqsM6leOIFazg==',
                                         'PBFPubKey': 'dummy', 'alg': '3DES-24'})

    def test_ussd_payment_exception(self):
        self.assertRaises(KeyError, Payment.ussd, self.card_payload, api=self.new_api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_tokenize_card(self, mock):
        path = 'flwv3-pug/getpaidx/api/tokenized/charge'
        Payment.tokenize_card(self.card_payload, self.new_api)
        mock.assert_called_once_with(path, self.new_api,
                                     {'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X', 'error': False,
                                      'cardno': '34343', 'cvv': '232', 'email': 'jb@gmail.com'})

    def test_tokenize_exception(self):
        self.assertRaises(KeyError, Payment.tokenize_card, self.mpesa_payload, api=self.new_api)

class TestBank(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )

    @patch('ravepaypysdk.resources.List.list')
    def test_get_all_banks(self, mock):
        path = '/flwv3-pug/getpaidx/api/flwpbf-banks.js?json=1'

        Bank.list_all(api=self.api)
        mock.assert_called_once_with(path, self.api)

    @patch('ravepaypysdk.resources.Create.create')
    def test_get_forex(self, mock):
        path = '/flwv3-pug/getpaidx/api/forex'
        payload = {
            'origin_currency': 'USD',
            'destination_currency': 'NGN',
            'amount': '200'
        }
        Bank.get_forex(payload, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'origin_currency': 'USD', 'destination_currency': 'NGN', 'amount': '200',
                'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X'}
        )


class TestPreauthorization(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )

    @patch('ravepaypysdk.resources.Create.create')
    def test_preauthorize_card(self, mock):
        path = '/flwv3-pug/getpaidx/api/charge'
        payload = dict(error=False, cardno='34343', cvv='232', email='jb@gmail.com')

        PreAuthorization.preauthorize_card(payload, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'client': b'Zah+qD4JviOdUFttZL7d0MgB/LPtEW4Gz7werMMDtOIWZLCGeZ7hRb0PlZbPU6JfELIgpyUP/L9ylb58B6EpXGPYHhYjC/Uza94nb4ZLiJM=',
                'PBFPubKey': 'dummy', 'alg': '3DES-24'}
        )

    @patch('ravepaypysdk.resources.Create.create')
    def test_capture(self, mock_capture):
        path = '/flwv3-pug/getpaidx/api/capture'
        payload = dict(error=False, email='jb@gmail.com')

        PreAuthorization.capture(payload, api=self.api)
        mock_capture.assert_called_once_with(
            path, self.api, {
                'error': False, 'email': 'jb@gmail.com',
                'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X'}
        )

    @patch('ravepaypysdk.helpers.Create.create')
    def test_void_refund(self, mock):
        path = '/flwv3-pug/getpaidx/api/refundorvoid'
        payload = dict(error=False, email='jb@gmail.com')

        PreAuthorization.void_or_refund(payload, api=self.api)
        mock.assert_called_once_with(
            path, self.api,
            {'error': False, 'email': 'jb@gmail.com', 'SECKEY': 'FLWSECK-cc8399cf35c2d1cfb62dd44c3c13f9ab-X'}
        )


class TestValidateCharge(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )
        self.payload = dict(error=False, cardno='34343', cvv='232', email='jb@gmail.com')
        self.card_path = '/flwv3-pug/getpaidx/api/validatecharge'
        self.account_path = '/flwv3-pug/getpaidx/api/validate'

    @patch('ravepaypysdk.helpers.Create.create')
    def test_card_validation(self, mock):
        ValidateCharge.card(self.payload, api=self.api)
        mock.assert_called_once_with(
            self.card_path, self.api, {
                'error': False, 'cardno': '34343', 'cvv': '232',
                'email': 'jb@gmail.com', 'PBFPubKey': 'dummy'}
        )

    @patch('ravepaypysdk.helpers.Create.create')
    def test_account_validation(self, mock):
        ValidateCharge.account(self.payload, api=self.api)
        mock.assert_called_once_with(
            self.account_path, self.api, {
                'error': False, 'cardno': '34343', 'cvv': '232',
                'email': 'jb@gmail.com', 'PBFPubKey': 'dummy'}
        )


class TestPaymentPlan(unittest.TestCase):
    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )
        self.payload = dict(id=70, name='johnbosco ohia')
        self.params = dict(id=70)
        self.plan_id = 20


    @patch('ravepaypysdk.helpers.Create.create')
    def test_create_payment_plan(self, mock):
        path = 'v2/gpx/paymentplans/create'
        PaymentPlan.create_plan(self.payload, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'id': 70, 'name': 'johnbosco ohia','seckey': self.api.secret_key
            })

    @patch('ravepaypysdk.helpers.List.list')
    def test_fetch_all_payment_plans(self, mock):
        path = 'v2/gpx/paymentplans/query'
        PaymentPlan.fetch_all_plan(api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'seckey': self.api.secret_key
            }
        )

    @patch('ravepaypysdk.helpers.List.list')
    def test_fetch_single_payment(self, mock):
        path = 'v2/gpx/paymentplans/query'
        PaymentPlan.fetch_single_plan(self.params, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'id': 70, 'seckey': self.api.secret_key
            }
        )

    @patch('ravepaypysdk.helpers.Create.create')
    def test_edit_plan(self, mock):
        path = 'v2/gpx/paymentplans/{}/edit'.format(self.plan_id)
        PaymentPlan.edit_plan(self.payload, self.plan_id, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'id': 70, 'name': 'johnbosco ohia', 'seckey': self.api.secret_key
            }
        )

    @patch('ravepaypysdk.helpers.Create.create')
    def test_edit_plan_without_payload(self, mock):
        path = 'v2/gpx/paymentplans/{}/edit'.format(self.plan_id)
        PaymentPlan.edit_plan(payload=None, plan_id=self.plan_id, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                 'seckey': self.api.secret_key
            }
        )

    @patch('ravepaypysdk.helpers.Create.create')
    def test_cancel_payment_plan(self, mock):
        path = 'v2/gpx/paymentplans/{}/cancel'.format(self.plan_id)
        PaymentPlan.cancel_plan(self.plan_id, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'seckey': self.api.secret_key
            }
        )

    def test_invalid_cancel_payment_plan(self):
        invalid_cancel_sub = PaymentPlan.cancel_plan(plan_id=None, api=self.api)
        self.assertEqual(None, invalid_cancel_sub)


class TestSubscriptions(unittest.TestCase):

    def setUp(self):
        self.api = Api(
            secret_key=os.environ.get('secret_key'),
            public_key='dummy',
            production=False
        )
        self.payload = dict(id=70, name='johnbosco ohia')
        self.params = dict(id=70)
        self.sub_id = 20


    @patch('ravepaypysdk.helpers.List.list')
    def test_fetch_all_subscriptions(self, mock):
        path =  'v2/gpx/subscriptions/query'
        Subscriptions.fetch_all(api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'seckey': self.api.secret_key
            }
        )
    @patch('ravepaypysdk.helpers.List.list')
    def test_fetch_single_subscription(self, mock):
        path = 'v2/gpx/subscriptions/query'
        Subscriptions.fetch_single(self.params, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'id': 70, 'seckey': self.api.secret_key
            }
        )

    def test_invalid_fetch_single_subscription(self):
        invalid_fetch_single_sub = Subscriptions.fetch_single(params=None, api=self.api)
        self.assertEqual(None, invalid_fetch_single_sub)

    @patch('ravepaypysdk.helpers.Create.create')
    def test_cancel_subscription(self, mock):
        path = 'v2/gpx/subscriptions/{}/cancel'.format(self.sub_id)
        Subscriptions.cancel(sub_id=self.sub_id, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'seckey': self.api.secret_key
            }
        )

    def test_invalid_cancel_subscription(self):
        invalid_cancel_sub = Subscriptions.cancel(sub_id=None, api=self.api)
        self.assertEqual(None, invalid_cancel_sub)


    @patch('ravepaypysdk.helpers.Create.create')
    def test_activate_subscription(self, mock):
        path = 'v2/gpx/subscriptions/{}/activate'.format(self.sub_id)
        Subscriptions.activate(sub_id=self.sub_id, api=self.api)
        mock.assert_called_once_with(
            path, self.api, {
                'seckey': self.api.secret_key
            }
        )

    def test_invalid_activate_subscription(self):
        invalid_activate_sub = Subscriptions.activate(sub_id=None, api=self.api)
        self.assertEqual(None, invalid_activate_sub)






