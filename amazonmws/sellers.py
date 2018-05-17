# coding: utf-8
"""
This module provides an implementation of the Amazon MWS Sellers API.
"""

__author__ = "Caleb P. Burns"
__created__ = "2012-12-03"
__modified__ = "2016-03-29"
__modified_by___ = "Joshua D. Burns"

import six # Python2/Python3 compatibility library.
import datetime
import amazonmws.mws
from amazonmws.util import datetime_to_iso8601

#: Actions.
ACTIONS = {
	'get_status': 'GetServiceStatus',
	'list_marketplaces': 'ListMarketplaceParticipations',
	'list_marketplaces_next': 'ListMarketplaceParticipationsByNextToken',
}


class MWSSellers(amazonmws.mws.MWS):
	"""
	The ``MWSSellers`` class is used to send requests to the Amazon MWS
	Sellers API. The primary purpose of this class is to allow sellers
	request information about their seller account.
	"""

	client_api_version = __modified__
	"""
	*client_api_version* (``str``) is the version of this client API.
	"""

	sellers_api_version = '2011-07-01'
	"""
	*sellers_api_version* (``str``) is the version of the MWS Sellers API
	implemented.
	"""

	path = "/Sellers/2011-07-01"
	"""
	*path* (``str``) is path all Sellers API requests are sent to.
	"""

	def get_status(self, debug=None):
		"""
		Requests the operational status of the Sellers API.

		Returns the response XML (``str``).
		"""
		args = self.new_args()
		args['Action'] = ACTIONS['get_status']
		return self.send_request(args, path=self.path, debug=debug)

	def list_marketplaces(self, debug=None):
		"""
		Requests the marketplaces the seller can sell in.

		Returns the response XML (``str``).
		"""
		args = self.new_args()
		args['Action'] = ACTIONS['list_marketplaces']
		return self.send_request(args, path=self.path, debug=debug)

	def list_marketplaces_next(self, next_token, debug=None):
		"""
		Requests the next batch of marketplaces the seller can sell in.

		*next_token* (``str``) is the token used to fetch the next batch of
		results.

		Returns the response XML (``str``).
		"""
		if not isinstance(next_token, six.string_types):
			raise TypeError("next_token:{!r} is not a str.".format(next_token))
		elif not next_token:
			raise ValueError("next_token:{!r} cannot be empty.".format(next_token))

		args = self.new_args()
		args['Action'] = ACTIONS['list_marketplaces_next']
		args['NextToken'] = next_token
		return self.send_request(args, path=self.path, debug=debug)

	def new_args(self):
		"""
		Returns a new ``dict`` of default arguments.
		"""
		return {
			'AWSAccessKeyId': self.access_key,
			'SellerId': self.merchant_id,
			'Timestamp': datetime_to_iso8601(datetime.datetime.utcnow()),
			'Version': self.sellers_api_version
		}
