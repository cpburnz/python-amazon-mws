# coding: utf-8
'''
This is a python implementation of the Orders API for the Amazon Marketplace Web Services(MWS).
This API inherits from MWS which supplies all the tools necessary to construct the proper
URL and send a request to Amazon MWS server.
This module consists of the necessary information to construct requests in the Orders API.
Calls include: ListOrders, ListOrdersByNextToken, GetOrder, ListOrderItems, ListOrderItems,
ListOrderItemsByNextToken, and GetServiceStatus.


Sample xml for a 'throttled' request:
HTTP ERROR 503

<?xml version="1.0"?>
<ErrorResponse xmlns="https://mws.amazonservices.com/Orders/2011-01-01">
  <Error>
    <Type>Sender</Type>
    <Code>RequestThrottled</Code>
    <Message>Request is throttled</Message>
  </Error>
  <RequestID>da90a758-492a-48bf-aae2-0f08e127e34b</RequestID>
</ErrorResponse>
'''

__date__ = "05/03/2012 10:04:37 AM"
__created__ = "2012-05-03"
__modified__ = "2013-03-28"

from amazonmws.mws import MWS#The MWS connection logic
from amazonmws.util import datetime_to_iso8601, is_sequence
import datetime
import re

#: Order statuses.
ORDER_STATUSES = {
	'cancelled': 'Canceled', # Yes, it is "Canceled" here and not "Cancelled".
	'invoice_unconfirmed': 'InvoiceUnconfirmed',
	'partially_shipped': 'PartiallyShipped',
	'pending': 'Pending',
	'shipped': 'Shipped',
	'unfulfillable': 'Unfulfillable',
	'unshipped': 'Unshipped',
}

class UnsupportedActionError(Exception):
	'''
	This exception is raised when an action is called
	that the Orders API doesn't support
	'''
	pass

class Orders( MWS ):
	'''
	The base class for all calls to the OrdersAPI
	This contains information pertaining to building a proper request query from
	the Orders API

	This class makes requests to the Amazon MWS Orders server by calling 'send_request'
	and passing it a supported `Action` with its given arguments.

	The arguments to pass with an action must follow these guidelines:
		- arguments are stored in a dict, where key is a parameter for the action
		  specified by the Orders API docs: `https://images-na.ssl-images-amazon.com/images/G/02/mwsportal/doc/en_US/orders/MWSOrdersApiReference._V136999359_.pdf` and value is either a single string value
		  for that parameter or a list of strings if that parameter can have multiple
		  values.
		- Do not include the 'Action' argument in the dict--this api will insert that for you
		- If the parameter can accept multiple values, ALWAYS put the value in a dict, even
		  if you're only passing a single value for that parameter.
		- It isn't necessary to supply args that is common to every Orders API call.
		  To tell what these args are, call Orders.new_args()

	Example args dict:
			for action 'ListOrders':
				args = {
					'CreatedAfter': '2012-05-03T15:00:13.000Z',
					'OrderStatus': ['Unshipped', 'PartiallyShipped'],
				}

			for action 'ListOrdersByNextToken':
				args = {
					'NextToken': 'jaiphegaueipraaegrajklh',
				}
	'''
	client_api_version = __modified__
	mws_api_version = '2011-01-01'
	path = '/Orders/2011-01-01' # The path to the server from the endpoint

	supported_actions = ('ListOrders', 'ListOrdersByNextToken', 'GetOrder', 'ListOrderItems', 'ListOrderItemsByNextToken', 'GetServiceStatus')#A list of supported actions in the Orders API

	def __init__(self, *args, **kwargs):
		MWS.__init__(self, *args, **kwargs)

	def new_args(self):
		'''
		Returns base query args for the Orders API--these
		items are used by each class
		'''
		return {
			'AWSAccessKeyId': self.access_key,
			'SellerId': self.merchant_id,
			'Timestamp': datetime_to_iso8601(datetime.datetime.utcnow()),
			'Version': self.mws_api_version
		}

	def send_request(self, action, args_dict):
		"""
		Send an Orders API request to the Amazon MWS server.
		Args:
			action[str]: an Orders API supported action. UnsupportActionError is raises if this is an unknown action
			args_dict[dict]: dictionary of arguments that follow the Orders API argument guidelines
		"""
		#Have to make the timestamp just before sending it out
		args = self.new_args()

		if action not in self.supported_actions:
			raise UnsupportedActionError( "UnsupportedActionError! '%s' is not a supported action in the Orders API, supported actions are: %s"% (action, self.supported_actions) )
		args['Action'] = action


		query = self._combine_dicts( args, args_dict )
		new_query = {}
		for key, value in query.iteritems():
			self._update_query( new_query, key, value )

		return MWS.send_request(self, new_query, path=self.path )

	def _combine_dicts(self, dict1, dict2):
		'''
		Safely combine two dicts' items, if the dict's have a key in common,
		if the value at that key in dict1 is a list, then value(s) from dict 2 are
		appended to the list, otherwise, if the value at the key in dict1 is
		a value, then the value in dict2 will overwrite it
		'''
		query = dict1
		for key, value in dict2.iteritems():
			if key in query:
				if isinstance( query[key], list ):
					if isinstance( value, list ):
						for item in value:
							query[key].append( item)
					else:
						query[key].append( value )
				else:
					query[key] = value
			else:
				#Update new key:value pair
				query[key] = value

		return query


	def _update_query( self, args, key, value ):
		'''
		Updates args with the new key, value
		If value is a list, then it flattens out the list into several keys:
			example:
				'MarketplaceId : [100,101,102]
					==>
				'MarketplaceId.Id.1: 100,
				'MarketplaceId.Id.2: 101,
				'MarketplaceId.Id.3: 102,
		'''
		if isinstance( value, list ):
			#Determine the base key
			basekey = self._get_key( key )
			for idx, val in enumerate(value):
				args[basekey + str(idx+1)] = val
		else:
			args[key] = value

	def _get_key(self, key):
		'''
		Determines the base keyname for keys that have a list as their value.
		This is necessary because these keys take up this notation:
			original key: 'MarketplaceId'
			new key: 'MarketplaceId.Id.x
			this function returns: 'MarketplaceId.Id.'
		'''
		item = None
		for item in re.finditer( r"([A-Z][a-z])+([a-z]+)?", key):
			pass
		item = item.group(0)#Get the last re.MatchObject from the iterator

		basekey = key + "." + item + "."
		return basekey

	def list_orders(self, created_after=None, updated_after=None, order_statuses=None, marketplaces=None):
		"""
		Requests the list of Orders that match the specified criteria.

		Either *created_after* or *updated_after* must be set, but not both.

		*created_after* (``datetime.datetime`` or ``float``) is used to
		select orders that were created at/after the specified date-time.

		*updated_after* (``datetime.datetime`` or ``float``) is used to
		select orders that were updated at/after the specified date-time.

		The query can be further refined by specifying any of the following:

		*order_statuses* (**sequence**) contains each Order Status (``str``)
		to filter the list of orders to list. Default is ``None`` for all
		Order Statuses.

		.. SEEALSO:: ``ORDER_STATUSES``.

		*marketplaces* (**sequence**) contains the ID (``str``) of each
		Amazon Marketplace to list orders from. Default is ``None`` for all
		Amazon Marketplaces.

		Returns the response XML (``str``).
		"""
		if (created_after is None and updated_after is None) or (created_after is not None and updated_after is not None):
			raise ValueError("Either created_after:{!r} or updated_after:{!r} must be set, but not both.".format(created_after, updated_after))

		args = self.new_args()

		if created_after is not None:
			args['CreatedAfter'] = datetime_to_iso8601(created_after, name='created_after')

		if updated_after is not None:
			args['LastUpdatedAfter'] = datetime_to_iso8601(updated_after, name='updated_after')

		if order_statuses is not None:
			if not is_sequence(order_statuses):
				raise TypeError("order_statuses:{!r} is not a sequence.".format(order_statuses))
			elif not order_statuses:
				raise ValueError("order_statuses:{!r} cannot be empty.".format(order_statuses))
			amazon_statuses = []
			for i, status in enumerate(order_statuses):
				status = ORDER_STATUSES.get(status, status)
				if not isinstance(status, basestring):
					raise TypeError("order_statuses[{}]:{!r} is not a string.".format(i, status))
				elif not status:
					raise ValueError("order_statuses[{}]:{!r} cannot be empty.".format(i, status))
				try:
					status = status.encode('ASCII')
				except UnicodeDecodeError as e:
					e.reason += " for order_statuses[{}]".format(i)
					e.args = e.args[:4] + (e.reason,)
					raise e
				amazon_statuses.append(status)
			args['OrderStatus'] = amazon_statuses

		if marketplaces is not None:
			if not is_sequence(marketplaces):
				raise TypeError("marketplaces:{!r} is not a sequence.".format(marketplaces))
			elif not marketplaces:
				raise ValueError("marketplaces:{!r} cannot be empty.".format(marketplaces))
			for i, market in enumerate(marketplaces):
				if not isinstance(market, basestring):
					raise TypeError("marketplaces[{}]:{!r} is not a string.".format(i, market))
				elif not market:
					raise ValueError("marketplaces[{}]:{!r} cannot be empty.".format(i, market))
				try:
					market = market.encode('ASCII')
				except UnicodeDecodeError as e:
					e.reason += " for marketplaces[{}]".format(i)
					e.args = e.args[:4] + (e.reason,)
					raise e
			args['MarketplaceId'] = marketplaces

		return self.send_request('ListOrders', args)

	def list_orders_next(self, next_token):
		"""
		Requests the next batch of Orders being listed.

		*next_token* (``str``) is the token used to fetch the next batch of
		results.

		Returns the response XML (``str``).
		"""
		if not isinstance(next_token, str):
			raise TypeError("next_token:{!r} is not a str.".format(next_token))
		elif not next_token:
			raise ValueError("next_token:{!r} cannot be empty.".format(next_token))

		args = self.new_args()
		args['NextToken'] = next_token

		return self.send_request('ListOrdersByNextToken', args)
