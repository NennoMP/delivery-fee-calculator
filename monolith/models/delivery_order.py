from datetime import datetime as dt
from marshmallow import Schema, fields, validate
from dataclasses import dataclass

class DeliveryOrderSchema(Schema):
    """Delivery Order model schema which allows to validate the parameters."""

    # Integer parameters cannot be smaller or equal than 0
    cart_value = fields.Integer(validate=validate.Range(min=1))
    delivery_distance = fields.Integer(validate=validate.Range(min=1))
    n_items = fields.Integer(validate=validate.Range(min=1))
    
    # Datetime must be ISO format and cannot be in the past
    order_time = fields.DateTime(
        format="%Y-%m-%dT%H:%M:%SZ",
        validate=lambda x: x.strftime('%Y-%m-%dT%H:%M:%SZ') > dt.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    )


@dataclass
class DeliveryOrder:
    "Representation of a Delivery Order model"

    # Attributes
    cart_value: int
    delivery_distance: int
    n_items: int
    order_time: str
