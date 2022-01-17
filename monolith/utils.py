import math
import pandas as pd
from datetime import datetime as dt


# GLOBALS
SPECIAL_DAY_RUSH = 4    # Friday
HOUR_START       = 15   # 3:00 PM
HOUR_END         = 19   # 7:00 PM


def check_payload_parameters(payload: dict) -> tuple[bool, str]:
    """Checks if all payloads parameters are valid.
    
    :param payload: dictionary containing all delivery order parameters
    :return: True or False, and (possibly) a custom error message
    """
    valid = True
    response = ''

    cart_value          = payload['cart_value']
    delivery_distance   = payload['delivery_distance']
    n_items             = payload['number_of_items']
    order_time          = dt.strptime(payload['time'], '%Y-%m-%dT%H:%M:%SZ')

    # Cart value negative or equal to 0
    if cart_value <= 0:
        valid = False
        response = '<cart_value> cannot be 0 or a negative integer'
    # Delivery distance negative or equal to 0
    elif delivery_distance <= 0:
        valid = False
        response = '<delivery_distance> cannot be 0 or a negative integer'
    # Number of items negative or equal to 0
    elif n_items <= 0:
        valid = False
        response = '<number_of_items> cannot be 0 or a negative integer'
    # Order datetime in the past
    elif order_time < dt.today():
        valid = False
        response = '<time> cannot be in the past'

    return valid, response


def is_friday_rush(order_datetime: str) -> bool:
    """Checks if the order datetime falls during the Friday rush.
    
    :param order_time: datetime of the delivery order
    :return: True or False
    """
    order_datetime = pd.Timestamp(order_datetime)

    # Check if the day of order datetime is Friday
    if order_datetime.dayofweek == SPECIAL_DAY_RUSH:
        # Check hourly range
        if order_datetime.hour >= HOUR_START and order_datetime.hour < HOUR_END:
            return True

    return False


def compute_delivery_fee(payload: dict) -> int:
    """Compute the total delivery fee of an order.
    
    :param payload: dictionary containing all delivery order parameters
    :return: total delivery fee
    """
    delivery_fee = 0

    cart_value          = payload['cart_value']
    delivery_distance   = payload['delivery_distance']
    n_items             = payload['number_of_items']

    # Multiplier for the Friday rush
    multiplier = 1

    # Check if cart value greater than 100€
    if cart_value < 10000:
        # Check if Friday rush
        if is_friday_rush(payload['time']):
            multiplier = 1.1 # update multiplier
        
        # Cart value fee (if smaller than 10€)
        if cart_value < 1000:
            delivery_fee += (1000 - cart_value)

        # Distance fee
        n_times = math.ceil(delivery_distance / 500)
        delivery_fee += (n_times * 100)

        # Number of items fee
        n = n_items - 4
        delivery_fee += (n * 50)

        delivery_fee *= multiplier
        # Check if total fee greater than 15€
        if delivery_fee > 1500:
            delivery_fee = 1500

    return int(delivery_fee)