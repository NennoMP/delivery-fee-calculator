import json
import math
import pandas as pd

# GLOBALS
file_settings = "monolith/settings.json"


class Calculator:
    """Calculator class that for computing the delivery fee of an order."""

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
    multiplier: int                 # multiplier to apply to total delivery fee in case of special rush weekday


    def __init__(self):
        # Load default parameters from a settings file
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

    def is_special_rush(self, order_datetime: str) -> bool:
        """Checks if the order datetime (day and hourly range) falls during the special rush.
        
        :param order_time: datetime of the delivery order
        :return: True or False
        """
        order_datetime = pd.Timestamp(order_datetime)

        # Check if the day of order datetime
        if order_datetime.dayofweek == self.special_rush_weekday:
            # Check hourly range
            if order_datetime.hour >= self.start_time and order_datetime.hour < self.end_time:
                return True

        return False

    def get_cart_fee(self, cart_value: int) -> int:
        """Compute the fee related to the cart value.
        
        :param cart_value: the cart value of the order
        :return: additional fee related to the cart value
        """

        cart_fee = 0
        # Check if cart value smaller than 10€
        if cart_value < self.min_order_no_surcharge:
            # Add fee
            cart_fee = self.min_order_no_surcharge - cart_value

        return cart_fee

    def get_distance_fee(self, delivery_distance: int) -> int:
        """Compute the fee related to the distance of the delivery.

        :param delivery_distance: the delivery distance of the order
        :return: additional fee related to the distance
        """

        # Number of distance blocks (500m) to which we add a fee
        n_times = math.ceil(delivery_distance / self.distance_block_size)
        return n_times * self.distance_fee

    def get_items_fee(self, n_items: int) -> int:
        """Compute the fee related to the number of items.
        
        :param n_items: the number of items of the order
        :return: additional fee related to the number of items
        """

        # Number of additional items (> 4) to the ones that are fee free
        n = n_items - self.n_items_free
        return n * self.item_fee

    def get_special_rush_fee(self, delivery_fee: int) -> int:
        """Compute the final delivery fee applying the special rush day multiplier.
        
        :param delivery_fee: current total delivery fee
        :return: total delivery fee after applying the multiplier
        """

        return delivery_fee * self.multiplier

    def compute_delivery_fee(self, payload: dict) -> int:
        """Compute the total delivery fee of an order.
        
        :param payload: dictionary containing all delivery order parameters
        :return: total delivery fee
        """

        delivery_fee = 0

        cart_value          = payload['cart_value']
        delivery_distance   = payload['delivery_distance']
        n_items             = payload['number_of_items']
        order_time          = payload['time']

        # Check if cart value greater than 100€
        if cart_value < self.min_order_free_delivery:
            
            # Add cart value fee
            delivery_fee += self.get_cart_fee(cart_value)

            # Add distance fee
            delivery_fee += self.get_distance_fee(delivery_distance)

            # Add number of items fee
            delivery_fee += self.get_items_fee(n_items)

            # Apply multiplier if special rush day
            if self.is_special_rush(order_time):
                delivery_fee = self.get_special_rush_fee(delivery_fee)

            # Total delivery fee cannot be greater than 15€
            delivery_fee = min(delivery_fee, self.max_fee)

        return int(delivery_fee)

    

    
