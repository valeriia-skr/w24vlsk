import app as app
import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_delivery_fee_invalid_cart_value(client):
    response = client.post('/calculate_fee', json={
        'cart_value': "invalid",  # Incorrect data type
        'number_of_items': 3,
        'order_time': '2024-01-18 12:00:00',
        'delivery_distance': 1000
    })
    assert response.status_code == 400
