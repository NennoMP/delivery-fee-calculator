from datetime import datetime as dt

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
    order_time          = payload['time']

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
    elif order_time < dt.today().strftime('%Y-%m-%dT%H:%M:%SZ'):
        valid = False
        response = '<time> cannot be in the past'

    return valid, response