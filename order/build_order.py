from marshmallow import Schema, fields, validate
from marshmallow import ValidationError

'''
- `symbol`: The trading symbol for the security to be traded (required)
- `qty`: The number of shares to be traded (required, must be greater than 0)
- `side`: The side of the trade, either 'buy' or 'sell' (required)
- `type`: The type of order, either 'market', 'limit', 'stop', or 'stop_limit' (required)
- `time_in_force`: The time in force for the order, either 'day', 'gtc', 'opg', 'cls', 'ioc', or 'fok' (required)
- `limit_price`: The limit price for a limit or stop_limit order (optional, must be greater than or equal to 0)
- `stop_price`: The stop price for a stop or stop_limit order (optional, must be greater than or equal to 0)

we will ignore the notional option and just use a mathematic expression to determine the qty to order based on pricing and order size
'''

class OrderSchema(Schema):
	symbol = fields.Str(required=True)
	qty = fields.Integer(required=True, validate=validate.Range(min=1))
	side = fields.Str(required=True, validate=validate.OneOf(['buy', 'sell']))
	type = fields.Str(required=True, validate=validate.OneOf(['market', 'limit', 'stop', 'stop_limit']))
	time_in_force = fields.Str(required=True,validate=validate.OneOf(['day', 'gtc', 'opg', 'cls', 'ioc', 'fok']))
	limit_price = fields.Float(validate=validate.Range(min=0))
	stop_price = fields.Float(validate=validate.Range(min=0))


def validate_order_request(request_data):
	schema = OrderSchema()
	try:
		schema.load(request_data)
	except ValidationError as err:
		return False, err.messages
	return True, None

