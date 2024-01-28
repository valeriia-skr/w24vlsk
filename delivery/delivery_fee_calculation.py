from delivery.delivery_parameters import DefaultDeliveryParameters
# for checking of order_time format
from datetime import datetime
# to ceil distance surcharge while calculating
import math


def convert_dollars_to_cents(value_in_dollars):
    value_in_cents = value_in_dollars*100
    return value_in_cents


class DeliveryFee(DefaultDeliveryParameters):
    """
    a class that contains a method for calculating standard delivery fee,
    can be expanded by other different methods or  modified by  modifying the default parameters
    """

    def __init__(self):
        super().__init__(base_delivery_fee=200,
                         base_item_surcharge=50,
                         bulk_surcharge=120,
                         item_threshold=5,
                         bulk_threshold=12,
                         friday=4,
                         rush_hour_start=15,
                         rush_hour_end=19,
                         cart_value_for_free_delivery=20000,
                         max_delivery_fee=1500
                         )

        self.full_delivery_fee = 0

    def calculate_delivery_fee(self, cart_value, number_of_items, order_time, delivery_distance):
        try:
            if cart_value < 0 or number_of_items < 0 or delivery_distance < 0:
                raise ValueError("Cart value, number of items, and delivery distance must be non-negative")

            if not isinstance(order_time, datetime):
                raise TypeError("Order time must be a datetime object")

            small_order_surcharge = SmallOrderSurcharge(cart_value).check_and_calculate()
            self.full_delivery_fee += small_order_surcharge

            free_delivery_due_to_cart = \
                FreeDeliveryDueToCart(cart_value, self.full_delivery_fee).check_and_calculate()
            self.full_delivery_fee = int(free_delivery_due_to_cart)

            if self.full_delivery_fee > 0:
                item_surcharge = ItemSurcharge(number_of_items).check_and_calculate()
                self.full_delivery_fee += item_surcharge

                distance_surcharge = DistanceSurcharge(delivery_distance).check_and_calculate()
                self.full_delivery_fee += distance_surcharge

                full_delivery_fee_due_to_rush_hour = \
                    FridayRushHourFee(order_time, self.full_delivery_fee).check_and_calculate()
                self.full_delivery_fee = full_delivery_fee_due_to_rush_hour

                delivery_fee_due_to_max = DeliveryFeeDueToMax(self.full_delivery_fee).check_and_calculate()
                if self.full_delivery_fee > delivery_fee_due_to_max:
                    self.full_delivery_fee = int(delivery_fee_due_to_max)

            return int(self.full_delivery_fee)

        except ValueError as e:
            print(f"ValueError occurred: {e}")

        except TypeError as e:
            print(f"TypeError occurred: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


class SmallOrderSurcharge(DeliveryFee):
    """
    a class that contains a method for calculating standard item small order surcharge-fee,
    can be expanded by other different methods or  modified by  adding/deleting parameters
    """

    def __init__(self, cart_value):
        super().__init__()
        self.cart_value = cart_value
        self.small_order_surcharge = 0

    def check_and_calculate(self):
        if self.cart_value < 1000:
            self.small_order_surcharge = 1000 - self.cart_value
        return int(self.small_order_surcharge)


class ItemSurcharge(DeliveryFee):
    """
    a class that contains a method for calculating standard item surcharge-fee,
    can be expanded by other different methods or  modified by  adding/deleting parameters
    """

    def __init__(self, number_of_items):
        super().__init__()
        self.number_of_items = number_of_items
        self.calculate_item_surcharge = 0

    def check_and_calculate(self):
        if self.number_of_items >= self.item_threshold:
            extra_items = self.number_of_items - 4
            self.calculate_item_surcharge += extra_items * self.base_item_surcharge
            if self.number_of_items > self.bulk_threshold:
                self.calculate_item_surcharge += self.bulk_surcharge
        return int(self.calculate_item_surcharge)


class DistanceSurcharge:
    """
    a class that contains a method for calculating standard item distance surcharge-fee,
    can be expanded by other different methods or  modified by  adding/deleting parameters
    """

    def __init__(self, delivery_distance):
        self.delivery_distance = delivery_distance
        self.distance_surcharge = 200

    def check_and_calculate(self):
        if self.delivery_distance > 1000:
            extra_distance_fee = self.delivery_distance - 1000

            self.distance_surcharge += convert_dollars_to_cents(math.floor(extra_distance_fee / 500))

        return int(self.distance_surcharge)


class FridayRushHourFee(DeliveryFee):
    """
    a class that contains a method for calculating standard item friday rush hour-fee,
    can be expanded by other different methods or  modified by  adding/deleting parameters
    """

    def __init__(self, order_time, full_delivery_fee):
        super().__init__()
        self.order_time = order_time
        self.full_delivery_fee = full_delivery_fee

    def check_and_calculate(self):
        if self.order_time.weekday() == self.friday and self.rush_hour_start <= \
                self.order_time.hour <= self.rush_hour_end:
            self.full_delivery_fee *= 1.2

        return int(self.full_delivery_fee)


class FreeDeliveryDueToCart(DeliveryFee):
    """
    a class that contains a method for calculating free delivery due to cart-fee,
    can be expanded by other different methods or  modified by  adding/deleting parameters
    """

    def __init__(self, cart_value, full_delivery_fee):
        super().__init__()
        self.cart_value = cart_value
        self.full_delivery_fee = full_delivery_fee

    def check_and_calculate(self):
        if self.cart_value >= self.cart_value_for_free_delivery:
            self.full_delivery_fee = 0
        return round(self.full_delivery_fee, 2)


class DeliveryFeeDueToMax(DeliveryFee):
    """
    a class that contains a method for calculating delivery fee due to max(delivery fee) -fee,
    can be expanded by other different methods or  modified by  adding/deleting parameters
    """

    def __init__(self, full_delivery_fee):
        super().__init__()
        self.full_delivery_fee = full_delivery_fee

    def check_and_calculate(self):
        if self.full_delivery_fee > self.max_delivery_fee:
            self.full_delivery_fee = self.max_delivery_fee

        return round(self.full_delivery_fee, 2)
