from flask import Blueprint, request, jsonify
from ..utils import check_payload_parameters
from .. import calculator as c


delivery = Blueprint('delivery', __name__)

calculator = c.Calculator()


@delivery.route('/delivery_calculator', methods=['POST'])
def delivery_calculator():
    """
    Manage the delivery fee costs of the orders.

        POST: compute and return total delivery fee
        :return: json response and status code
        - 200: returned delivery fee
        - 422: invalid parameters in body
    """

    payload = request.get_json()
    if request.method == 'POST':
        valid, message = check_payload_parameters(payload)
        if not valid:
            response = {
                'status': 'Failed',
                'message': message,
            }
            return jsonify(response), 422

        delivery_fee = calculator.compute_delivery_fee(payload)
        response = {
            'status': 'Success',
            'delivery_fee': delivery_fee
        }
                
    return jsonify(response), 200
        

        

