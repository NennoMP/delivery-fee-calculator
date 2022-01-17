import json
import math
import pandas as pd

# GLOBALS
file_settings = "monolith/settings.json"


class Calculator:
    """Class that implements auxiliary functions for computing the total   delivery fee.
    """
    # Attributes
    min_order_no_surcharge: int     # min cart value with no surcharge
    min_order_free_delivery: int    # min cart value for free delivery

    distance_block_size: int        # number of meters for additional fee
    distance_fee: int               # fee for each distance block
    n_items_free: int               # number of items with no surcharge
    item_fee: int                   # fee for additional items
    max_fee: int                    # maximum fee possible

    # (0-6 | Monday-Sunday)
    special_rush_weekday: int       # weekday with special rush
    # 24h format
    start_time: int
    end_time: int
    multiplier: int                 # multiplier to apply to total delivery


    def __init__(self):
        with open(file_settings) as inf:
            file = json.load(inf)

            self.min_order_no_surcharge = file['delivery_fees']['min_order_no_surcharge']
            self.min_order_free_delivery = file['delivery_fees']['min_order_free_delivery']

            self.distance_block_size = file['delivery_fees']['distance_block_size']
            self.distance_fee = file['delivery_fees']['distance_fee']
            self.n_items_free = file['delivery_fees']['n_items_fee_free']
            self.item_fee = file['delivery_fees']['item_fee']
            self.max_fee = file['delivery_fees']['max_fee']

            self.special_rush_weekday = file['special_rush']['weekday']
            self.start_time = file['special_rush']['start_time']
            self.end_time = file['special_rush']['end_time']
            self.multiplier = file['special_rush']['multiplier']

    def is_friday_rush(self, order_datetime: str) -> bool:
        """Checks if the order datetime falls during the Friday rush.
        
        :param order_time: datetime of the delivery order
        :return: True or False
        """
        order_datetime = pd.Timestamp(order_datetime)

        # Check if the day of order datetime is Friday
        if order_datetime.dayofweek == self.special_rush_weekday:
            # Check hourly range
            if order_datetime.hour >= self.start_time and order_datetime.hour < self.end_time:
                return True

        return False

    def compute_delivery_fee(self, payload: dict) -> int:
        """Compute the total delivery fee of an order.
        
        :param payload: dictionary containing all delivery order parameters
        :return: total delivery fee
        """
        delivery_fee = 0

        cart_value          = payload['cart_value']
        delivery_distance   = payload['delivery_distance']
        n_items             = payload['number_of_items']
        order_time          = payload['time]

        # Multiplier for the Friday rush
        multiplier = 1

        # Check if cart value greater than 100€
        if cart_value < self.min_order_free_delivery:
            # Check if special rush weekday
            if self.is_friday_rush(order_time):
                multiplier = self.multiplier # update multiplier
            
            # Cart value fee (if smaller than 10€)
            if cart_value < self.min_order_no_surcharge:
                delivery_fee += (self.min_order_no_surcharge - cart_value)

            # Distance fee
            n_times = math.ceil(delivery_distance / self.distance_block_size)
            delivery_fee += (n_times * self.distance_fee)

            # Number of items fee
            n = n_items - self.n_items_free
            delivery_fee += (n * self.item_fee)

            delivery_fee *= multiplier
            # Check if total fee greater than 15€
            if delivery_fee > self.max_fee:
                delivery_fee = self.max_fee

        return int(delivery_fee)

    
