import pytest

from logistic.models import Product

BASE_URL = '/api/v1/products/'


@pytest.mark.django_db
def test_get_products(client, product_factory, stock_factory):

    products = product_factory(_quantity=5)
    stocks = stock_factory(_quantity=2, products=products)
    url = BASE_URL + str(stocks[0].id) + '/'
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data['id'] == stocks[0].id

