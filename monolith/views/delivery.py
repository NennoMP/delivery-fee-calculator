from flask import Blueprint, request, jsonify
from .. import calculator as c
from marshmallow import ValidationError
from dataclasses import asdict

from ..models.delivery_order import DeliveryOrderSchema, DeliveryOrder

delivery = Blueprint('delivery', __name__)
calculator = c.Calculator()


@delivery.route('/delivery_calculator', methods=['POST'])
def delivery_calculator():
    """
    Manage the delivery fee costs of an order.

        POST: compute and return total delivery fee
        :return: json response and status code
        - 200: returned delivery fee
        - 422: invalid parameters in body
    """

    if request.method == 'POST':
        payload = request.get_json()

        try:
            delivery_order = DeliveryOrder(
                cart_value=payload['cart_value'],
                delivery_distance=payload['delivery_distance'],
                n_items=payload['number_of_items'],
                time=payload['time']
            )
            DeliveryOrderSchema().load(asdict(delivery_order))
        except ValidationError as ve:
            response = {
                'status': 'Failed',
                'message': ve.messages
            }
            return jsonify(response), 422

        delivery_fee = calculator.compute_delivery_fee(payload)
        response = {
            'status': 'Success',
            'delivery_fee': delivery_fee
        }
                    
        return jsonify(response), 200
        

        

