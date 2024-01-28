import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Invalid value for cart_value
def test_get_delivery_fee_invalid_cart_value(client):
    response = client.post('/calculate_fee', json={
        'cart_value': "invalid",  # Incorrect data type
        'number_of_items': 3,
        'order_time': '2024-01-18 12:00:00',
        'delivery_distance': 1000
    })
    assert response.status_code == 400


# Invalid value for number_of_items
def test_get_delivery_fee_invalid_number_of_items(client):
    response = client.post('/calculate_fee', json={
        'cart_value': 50,
        'number_of_items': -1,  # Invalid value
        'order_time': '2024-01-18 12:00:00',
        'delivery_distance': 1000
    })
    assert response.status_code == 400


# Invalid value for order_time
def test_get_delivery_fee_invalid_order_time(client):
    response = client.post('/calculate_fee', json={
        'cart_value': 50,
        'number_of_items': 3,
        'order_time': 'not-a-datetime',  # Incorrect date format
        'delivery_distance': 1000
    })
    assert response.status_code == 400


# Invalid value for delivery_distance
def test_get_delivery_fee_invalid_delivery_distance(client):
    response = client.post('/calculate_fee', json={
        'cart_value': 50,
        'number_of_items': 3,
        'order_time': '2024-01-18 12:00:00',
        'delivery_distance': "invalid"  # Incorrect data type
    })
    assert response.status_code == 400


# Missing cart_value
def test_get_delivery_fee_missing_cart_value(client):
    response = client.post('/calculate_fee', json={
        # 'cart_value' is missing
        'number_of_items': 3,
        'order_time': '2024-01-18 12:00:00',
        'delivery_distance': 1000
    })
    assert response.status_code == 400


# Incorrect time for rush hour check
def test_get_delivery_fee_rush_hour(client):
    response = client.post('/calculate_fee', json={
        'cart_value': 50,
        'number_of_items': 3,
        'order_time': '2024-01-18 16:00:00',  # Rush hour time
        'delivery_distance': 1000
    })
    assert response.status_code == 200


# Testing free delivery at a certain cart value threshold
def test_get_delivery_fee_free_delivery_threshold(client):
    response = client.post('/calculate_fee', json={
        'cart_value': 200,  # Threshold for free delivery
        'number_of_items': 3,
        'order_time': '2024-01-18 12:00:00',
        'delivery_distance': 1000
    })
    assert response.status_code == 200
    assert response.json == {"delivery_fee": 0}