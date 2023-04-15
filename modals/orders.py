from marshmallow import Schema, fields, validate

'''
This module checks order dictionaries for validation against the alpaca api accepted parameters. Anything out of range that would throw an api error will not pass validation.
'''

# Define the order schema for stocks using marshmallow
class StockOrderSchema(Schema):
	symbol = fields.Str(required=True)
	qty = fields.Integer(required=True, validate=validate.Range(min=1))
	side = fields.Str(required=True, validate=validate.OneOf(["buy", "sell"]))
	type = fields.Str(required=True, validate=validate.OneOf(["market", "limit", "stop", "stop_limit"]))
	time_in_force = fields.Str(required=True, validate=validate.OneOf(["gtc", "opg", "ioc", "fok"]))
	limit_price = fields.Float(validate=validate.Range(min=0))
	stop_price = fields.Float(validate=validate.Range(min=0))
	trail_price = fields.Float(validate=validate.Range(min=0))
	client_order_id = fields.Str(validate=validate.Length(max=48))
	order_class = fields.Str(validate=validate.OneOf(["simple", "bracket", "oco", "oto"]))
	take_profit = fields.Float(validate=validate.Range(min=0))
	stop_loss = fields.Float(validate=validate.Range(min=0))
	
# Define the order schema for crypto using marshmallow
class CryptoOrderSchema(Schema):
	symbol = fields.Str(required=True)
	qty = fields.Integer(required=True, validate=validate.Range(min=1))
	side = fields.Str(required=True, validate=validate.OneOf(["buy", "sell"]))
	type = fields.Str(required=True, validate=validate.OneOf(["market", "limit", "stop_limit"]))
	time_in_force = fields.Str(required=True, validate=validate.OneOf(["gtc", "ioc"]))
	limit_price = fields.Float(validate=validate.Range(min=0))
	stop_price = fields.Float(validate=validate.Range(min=0))
	trail_price = fields.Float(validate=validate.Range(min=0))
	client_order_id = fields.Str(validate=validate.Length(max=48))
	order_class = fields.Str(validate=validate.OneOf(["simple", "bracket", "oco", "oto"]))
	take_profit = fields.Float(validate=validate.Range(min=0))
	stop_loss = fields.Float(validate=validate.Range(min=0))
	
# this function validates stock orders
def validate_stock_order(order):
	order_schema = StockOrderSchema()
	errors = order_schema.validate(order)
	if errors:
	print(errors)  # Handle validation errors
	else:
		return order

# this function validates crypto orders
def validate_crypto_order(order):
	order_schema = CryptoOrderSchema()
	errors = order_schema.validate(order)
	if errors:
	print(errors)  # Handle validation errors
	else:
		return order

