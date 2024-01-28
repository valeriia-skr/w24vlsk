"""
Default parameter-settings that we'll use in delivery calculations,
values should be then pre-known by the implementation manager/programmer
"""


class DefaultDeliveryParameters:
    def __init__(self,
                 base_delivery_fee=0,
                 base_item_surcharge=0,
                 bulk_surcharge=0,
                 item_threshold=0,
                 bulk_threshold=0,
                 friday=0,
                 rush_hour_start=0,
                 rush_hour_end=0,
                 cart_value_for_free_delivery=0,
                 max_delivery_fee=0
                 ):
        self.base_delivery_fee = base_delivery_fee
        self.base_item_surcharge = base_item_surcharge
        self.bulk_surcharge = bulk_surcharge
        self.item_threshold = item_threshold
        self.bulk_threshold = bulk_threshold
        self.max_delivery_fee = max_delivery_fee
        self.friday = friday
        self.rush_hour_start = rush_hour_start
        self.rush_hour_end = rush_hour_end
        self.cart_value_for_free_delivery = cart_value_for_free_delivery
