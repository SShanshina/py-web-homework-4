import pytest
from rest_framework.test import APIClient
from logistic.models import Product, Stock, StockProduct

BASE_URL_1 = '/api/v1/products/'
BASE_URL_2 = '/api/v1/stocks/'


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_post_product(client):
    product = Product(title='Яблоки', description='Сладкие')
    product.save()
    url = BASE_URL_1 + str(product.id) + '/'
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data['title'] == product.title


@pytest.mark.django_db
def test_post_stock(client):
    product_1 = Product(title='Клубничный джем', description='Без консервантов')
    product_1.save()
    product_2 = Product(title='Печенье', description='С шоколадной крошкой')
    product_2.save()
    position_1 = {
                'product': product_1,
                'quantity': 99,
                'price': 149.80
            }
    position_2 = {
                'product': product_2,
                'quantity': 20,
                'price': 218.50
            }
    stock = Stock.objects.create(address='ул. Сиреневая, 1')
    StockProduct.objects.create(stock=stock, **position_1)
    stock.positions.create(**position_2)

    url = BASE_URL_2 + str(stock.id) + '/'
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data['address'] == 'ул. Сиреневая, 1'
    assert data['positions'][0]['product'] == product_1.id
    assert data['positions'][1]['quantity'] == position_2['quantity']
