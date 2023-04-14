import datetime
from django.test import TestCase, Client
from currency import views
from decimal import Decimal
from currency.models import Currency


class MakeRequestTestCase(TestCase):
    def test_old_date(self):
        date = datetime.datetime(2023, 4, 13)
        data = views.make_request_to_cb(date)
        self.assertEqual(data, {'EUR': Decimal('89.76'), 'USD': Decimal('82.09')})

    def test_wrong_date(self):
        date = '2022-12-14'
        data = views.make_request_to_cb(date)
        self.assertEqual(data, None)


class GetCurrencyTestCase(TestCase):
    def setUp(self):
        self.date_check = datetime.datetime(2023, 4, 13)
        Currency.objects.filter(date=self.date_check).delete()

    def test_old_date(self):
        date = datetime.datetime(2023, 4, 13)
        data = views.get_currency(date)
        self.assertEqual(data, {'EUR': Decimal('89.76'), 'USD': Decimal('82.09')})

    def check_in_db(self):
        data = Currency.objects.filter(date=self.date_check).values('EUR', 'USD')[0]
        self.assertEqual(data, {'EUR': Decimal('89.76'), 'USD': Decimal('82.09')})

    def test_wrong_date(self):
        date = '2022-12-14'
        data = views.get_currency(date)
        self.assertEqual(data, None)


class ShowCurrencyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_show_currency_future(self):
        response = self.client.get('/ajax/get-currency', {'date': '2024-4-5'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),  {'EUR': 'поживем увидим', 'USD': 'поживем увидим'})

    def test_show_currency_past(self):
        response = self.client.get('/ajax/get-currency', {'date': '2023-4-13'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),  {'EUR': '89.76', 'USD': '82.09'})

    def test_show_currency_wrong_date(self):
        response = self.client.get('/ajax/get-currency', {'date': '2023'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  {'error': 'неправильный формат данных. Должен быть ...?date=2023-04-10'})


class CheckFirstPage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_first_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'currency_template.html')
