from django.shortcuts import render
from django.http import JsonResponse
import datetime
from .models import Currency
import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def check_date(func):
    def _wrapper(*args, **kwargs):
        date = args[0]
        if not isinstance(date, datetime.date):
            return None
        result = func(*args, **kwargs)
        return result
    return _wrapper


def start_page(request, template):
    return render(request, template)


@check_date
def make_request_to_cb(date: datetime) -> dict:
    '''
    make a request to Central Bank Russia
    :param date: requested date
    :return: {'EUR': 84.44 , 'USD': 73.45}
    '''
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': date.strftime("%d/%m/%Y")})
    soup = BeautifulSoup(response.content, "html.parser")
    data = dict()
    for line in soup.find_all('charcode'):
        if line.text == 'EUR' or line.text == 'USD':
            data_cur = line.parent
            val_cur = Decimal(data_cur.find('value').text.replace(',', '.'))
            num_cur = Decimal(data_cur.find('nominal').text.replace(',', '.'))
            data[line.text] = Decimal(val_cur/num_cur).quantize(Decimal('0.00'))
    return data


@check_date
def get_currency(date: datetime) -> dict:
    '''
    check that currency in the DB in other case make a request
    :param date: requested date
    :return: {'EUR': 84.44 , 'USD': 73.45}
    '''
    data = Currency.objects.filter(date=date)
    if not data:
        data = make_request_to_cb(date)
        Currency.objects.create(date=date, EUR=data['EUR'], USD=data['USD'])
    else:
        data = data.values('EUR', 'USD')[0]
    return data


def show_currency(request) -> JsonResponse:
    '''
    send to AJAX dict to be rendered
    request = /ajax/get-currency?date=2023-04-10
    return {'EUR': 84.44 , 'USD': 73.45}
    '''
    try:
        date = datetime.datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
    except:
        return JsonResponse(data={'error': 'неправильный формат данных. Должен быть ...?date=2023-04-10'}, status=400)
    if date > datetime.datetime.now().date():
        data = {'EUR': 'поживем увидим', 'USD': 'поживем увидим'}
    else:
        data = get_currency(date)
    if not data:
        return JsonResponse(data={'error': 'Ошибка сервиса'}, status=404)
    return JsonResponse(data=data, status=200)
