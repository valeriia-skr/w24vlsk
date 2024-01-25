from delivery.delivery_fee_calculation import DeliveryFee

"""
Fabric-function to create a single calculation for a better async. processes' control 
"""


def generate_new_delivery_fee_calculation():
    new_delivery_fee = DeliveryFee()
    return new_delivery_fee
