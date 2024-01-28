"""
Testing Invalid Input Values
"""
import pytest
from datetime import datetime
from delivery.delivery_fee_calculation import (DeliveryFee, ItemSurcharge, SmallOrderSurcharge,
                                               DistanceSurcharge, FridayRushHourFee,
                                               DeliveryFeeDueToMax, FreeDeliveryDueToCart
                                               )


# Testing DeliveryFee
@pytest.mark.parametrize("cart_value, number_of_items, order_time, delivery_distance, expected_fee", [
    (890, 1, datetime(2024, 1, 18, 12, 0, 0), 1000, 110 + 200),  # 1.10e small order surcharge + 2e base distance
    (50, 5, datetime(2024, 1, 18, 12, 0, 0), 1000, 950 + 50 + 200),  # 9.5e small order surcharge + 0.50e item
    # surcharge + 2e base distance
    (50, 1, datetime(2024, 1, 18, 12, 0, 0), 1500, 950 + 200 + 100),  # 9.5e small order surcharge + 2e base + 1e for
    # 500m
    (50, 20, datetime(2024, 1, 18, 12, 0, 0), 3000, 1500),  # Exceeds 15e but capped
    (20000, 1, datetime(2024, 1, 18, 12, 0, 0), 1000, 0),  # Free delivery
    (50, 1, datetime(2024, 1, 19, 16, 0, 0), 1000, (950 + 200) * 1.2)  # 9.5e small order surcharge + 2e bace * 1.2x
    # friday rush hour multiplier
])
def test_delivery_fee(cart_value, number_of_items, order_time, delivery_distance, expected_fee):
    delivery_fee = DeliveryFee()
    assert delivery_fee.calculate_delivery_fee(cart_value, number_of_items,
                                               order_time, delivery_distance) == expected_fee


# Testing SmallOrderSurcharge
@pytest.mark.parametrize("cart_value, expected_surcharge", [
    (50, 950),
    (890, 110),
    (1000, 0),
    (999, 1)
])
def test_small_order_surcharge(cart_value, expected_surcharge):
    surcharge = SmallOrderSurcharge(cart_value)
    assert surcharge.check_and_calculate() == expected_surcharge


# Testing DistanceSurcharge
@pytest.mark.parametrize("distance, expected_surcharge", [
    (1000, 200),
    (1499, 200),
    (1500, 201),
    (1501, 201)
])
def test_distance_surcharge(distance, expected_surcharge):
    surcharge = DistanceSurcharge(distance)
    assert surcharge.check_and_calculate() == expected_surcharge


# Testing ItemSurcharge
@pytest.mark.parametrize("number_of_items, expected_surcharge", [
    (4, 0),
    (5, 50),
    (10, 300),
    (13, 570),
    (14, 620)
])
def test_item_surcharge(number_of_items, expected_surcharge):
    surcharge = ItemSurcharge(number_of_items)
    assert surcharge.check_and_calculate() == expected_surcharge


# Testing FridayRushHourFee
@pytest.mark.parametrize("order_time, full_delivery_fee, expected_surcharge", [
    (datetime(2024, 1, 19, 16, 0, 0), 1000, 1200),  # Friday during rush hour
    (datetime(2024, 1, 19, 20, 0, 0), 1000, 1000),  # Friday outside rush hour
    (datetime(2024, 1, 18, 16, 0, 0), 1000, 1000),  # Not Friday
])
def test_friday_rush_hour_fee(order_time, full_delivery_fee, expected_surcharge):
    rush_hour_fee = FridayRushHourFee(order_time, full_delivery_fee)
    assert rush_hour_fee.check_and_calculate() == expected_surcharge


# Testing FreeDeliveryDueToCart
@pytest.mark.parametrize("cart_value, full_delivery_fee, expected_delivery_fee", [
    (25000, 2000, 0),  # When above threshold
    (15000, 2000, 2000)  # When below threshold
])
def test_free_delivery(cart_value, full_delivery_fee, expected_delivery_fee):
    delivery_fee_free = FreeDeliveryDueToCart(cart_value, full_delivery_fee)
    assert delivery_fee_free.check_and_calculate() == expected_delivery_fee


# Testing DeliveryFeeDueToMax
@pytest.mark.parametrize("full_delivery_fee, expected_fee", [
    (1600, 1500),  # Case where the initial delivery fee exceeds the maximum
    (1400, 1400)  # Case where the initial delivery fee is below the maximum
])
def test_delivery_fee_due_to_max(full_delivery_fee, expected_fee):
    delivery_fee_max = DeliveryFeeDueToMax(full_delivery_fee)
    assert delivery_fee_max.check_and_calculate() == expected_fee
