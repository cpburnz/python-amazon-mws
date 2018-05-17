# coding: utf-8
from __future__ import division
"""
This module provides an implementation of the Amazon MWS Products API.
"""

__author__ = "Caleb P. Burns"
__created__ = "2012-12-04"
__modified__ = "2016-03-29"
__modified_by___ = "Joshua D. Burns"

import six # Python2/Python3 compatibility library.
import datetime
import amazonmws.mws
from amazonmws.util import datetime_to_iso8601, is_sequence

#: Actions.
ACTIONS = {
	'list_matching': 'ListMatchingProducts',
	'get_products_for_id': 'GetMatchingProductForId',
	'get_competitive_pricing_for_sku': 'GetCompetitivePricingForSKU',
	'get_competitive_pricing_for_asin': 'GetCompetitivePricingForASIN',
	'get_lowest_listings_for_sku': 'GetLowestOfferListingsForSKU',
	'get_lowest_listings_for_asin': 'GetLowestOfferListingsForASIN',
	'get_my_price_for_sku': 'GetMyPriceForSKU',
	'get_my_price_for_asin': 'GetMyPriceForASIN',
	'get_categories_for_sku': 'GetProductCategoriesForSKU',
	'get_categories_for_asin': 'GetProductCategoriesForASIN'
}

#: Maximum number of requests before being throttled.
THROTTLE_MAX_REQUESTS = {
	'list_matching': 20,
	'get_products_for_id': 20,
	'get_competitive_pricing_for_sku': 20,
	'get_competitive_pricing_for_asin': 20,
	'get_lowest_listings_for_sku': 20,
	'get_lowest_listings_for_asin': 20,
	'get_my_price_for_sku': 20,
	'get_my_price_for_asin': 20,
	'get_categories_for_sku': 20,
	'get_categories_for_asin': 20
}

#: The number of seconds it takes to restore 1 request from the quota.
THROTTLE_RESTORE_RATES = {
	'list_matching': 5,
	'get_products_for_id': 1 / 5,
	'get_competitive_pricing_for_sku': 1 / 10,
	'get_competitive_pricing_for_asin': 1 / 10,
	'get_lowest_listings_for_sku': 1 / 10,
	'get_lowest_listings_for_asin': 1 / 10,
	'get_my_price_for_sku': 1 / 10,
	'get_my_price_for_asin': 1 / 10,
	'get_categories_for_sku': 5,
	'get_categories_for_asin': 5
}

#: ID types.
ID_TYPES = {
	'asin': 'ASIN',
	'ean': 'EAN',
	'isbn': 'ISBN',
	'jan': 'JAN',
	'sku': 'SellerSKU',
	'upc': 'UPC'
}

#: Item conditions.
ITEM_CONDITIONS = {
	'new': 'New',
	'used': 'Used',
	'collectible': 'Collectible',
	'refurbished': 'Refurbished',
	'club': 'Club'
}

#: Query contexts.
QUERY_CONTEXTS = {
	'all': 'All',
	'apparel': 'Apparel',
	'appliances': 'Appliances',
	'arts_and_crafts': 'ArtsAndCrafts',
	'automotive': 'Automotive',
	'baby': 'Baby',
	'beauty': 'Beauty',
	'books': 'Books',
	'classical': 'Classical',
	'digital_music': 'DigitalMusic',
	'dvd': 'DVD',
	'electronics': 'Electronics',
	'foreign_books': 'ForeignBooks',
	'garden': 'Garden',
	'grocery': 'Grocery',
	'health_personal_care': 'HealthPersonalCare',
	'hobbies': 'Hobbies',
	'home': 'Home',
	'home_garden': 'HomeGarden',
	'home_improvement': 'HomeImprovement',
	'industrial': 'Industrial',
	'jewelry': 'Jewelry',
	'kindle_store': 'KindleStore',
	'kitchen': 'Kitchen',
	'lighting': 'Lighting',
	'magazines': 'Magazines',
	'miscellaneous': 'Miscellaneous',
	'mobile_apps': 'MobileApps',
	'mp3_downloads': 'MP3Downloads',
	'music': 'Music',
	'musical_instruments': 'MusicalInstruments',
	'music_tracks': 'MusicTracks',
	'office_products': 'OfficeProducts',
	'outdoor_living': 'OutdoorLiving',
	'outlet': 'Outlet',
	'pc_hardware': 'PCHardware',
	'pet_supplies': 'PetSupplies',
	'photo': 'Photo',
	'shoes': 'Shoes',
	'software': 'Software',
	'software_video_games': 'SoftwareVideoGames',
	'sporting_goods': 'SportingGoods',
	'tools': 'Tools',
	'toys': 'Toys',
	'unbox_video': 'UnboxVideo',
	'vhs': 'VHS',
	'video': 'Video',
	'video_games': 'VideoGames',
	'watches': 'Watches',
	'wireless': 'Wireless',
	'wireless_accessories': 'WirelessAccessories'

}


class MWSProducts(amazonmws.mws.MWS):
	"""
	The ``MWSProducts`` class is used to send requests to the Amazon MWS
	Products API. The primary purpose of this class is to allow sellers to
	get information about products on Amazon that match a seller's
	existing products.
	"""

	client_api_version = __modified__
	"""
	*client_api_version* (``str``) is the version of this client API.
	"""

	products_api_version = '2011-07-01'
	"""
	*products_api_version* (``str``) is the version of the MWS Products
	API implemented.
	"""

	path = "/Products/2011-10-01"
	"""
	*path* (``str``) is path all Sellers API requests are sent to.
	"""

	def get_categories(self, marketplace_id, id_type, id_, verbose=None):
		"""
		Requests the categories for the specified marketplace product.

		*marketplace_id* (``str``) is the ID of the Amazon Marketplace the
		products belong to.

		*id_type* (``str``) is the type of ID used. This can only be
		"ASIN" or "SellerSKU".

		*id_* (``str``) is either the ASIN or SKU of the product.

		Returns the response XML (``str``).
		"""
		if not isinstance(marketplace_id, six.string_types):
			raise TypeError("marketplace_id:{!r} is not a str.".format(marketplace_id))
		elif not marketplace_id:
			raise ValueError("marketplace_id:{!r} cannot be empty.".format(marketplace_id))

		if not isinstance(id_type, six.string_types):
			raise TypeError("id_type:{!r} is not a str.".format(id_type))
		elif not id_type:
			raise ValueError("id_type:{!r} cannot be empty.".format(id_type))

		if not isinstance(id_, six.string_types):
			raise TypeError("id_:{!r} is not a str.".format(id_))
		elif not id_:
			raise ValueError("id_:{!r} cannot be empty.".format(id_))

		args = self.new_args()
		if id_type == 'ASIN':
			args['Action'] = ACTIONS['get_my_price_for_asin']
			args['ASIN'] = id_
		elif id_type == 'SellerSKU':
			args['Actions'] = ACTIONS['get_my_price_for_sku']
			args['SellerSKU'] = id_
		else:
			raise ValueError("id_type:{!r} is not 'ASIN' or 'SellerSKU'.".format(id_type))

		return self.send_request(args, path=self.path, verbose=verbose)

	def get_competitive_pricing(self, marketplace_id, id_type, id_list, verbose=None):
		"""
		Requests the competitive pricing for the specified marketplace
		products.

		*marketplace_id* (``str``) is the ID of the Amazon Marketplace the
		products belong to.

		*id_type* (``str``) is the type of ID used. This can only be
		"ASIN" or "SellerSKU".

		*id_list* (**sequence**) contains the ID (``str``) of each product
		to get. A maximum of 20 IDs can be requested at a single time.

		Returns the response XML (``str``).
		"""
		if not isinstance(marketplace_id, six.string_types):
			raise TypeError("marketplace_id:{!r} is not a str.".format(marketplace_id))
		elif not marketplace_id:
			raise ValueError("marketplace_id:{!r} cannot be empty.".format(marketplace_id))

		if not isinstance(id_type, six.string_types):
			raise TypeError("id_type:{!r} is not a str.".format(id_type))
		elif not id_type:
			raise ValueError("id_type:{!r} cannot be empty.".format(id_type))

		if not is_sequence(id_list):
			raise TypeError("id_list:{!r} is not a sequence.".format(id_list))
		elif not id_list:
			raise ValueError("id_list:{!r} cannot be empty.".format(id_list))
		elif len(id_list) > 20:
			raise ValueError("id_list length:{} cannot be greater than 20.".format(len(id_list)))

		args = self.new_args()
		args['IdType'] = id_type
		if id_type == 'ASIN':
			args['Action'] = ACTIONS['get_competitive_pricing_for_asin']
			args.update({'ASINList.ASIN.{}'.format(i): asin for i, asin in enumerate(id_list, 1)})
		elif id_type == 'SellerSKU':
			args['Actions'] = ACTIONS['get_competitive_pricing_for_sku']
			args.update({'SellerSKUList.SellerSKU.{}'.format(i): sku for i, sku in enumerate(id_list, 1)})
		else:
			raise ValueError("id_type:{!r} is not 'ASIN' or 'SellerSKU'.".format(id_type))

		return self.send_request(args, path=self.path, verbose=verbose)

	def get_lowest_listings(self, marketplace_id, id_type, id_list, condition=None, exclude_me=None, verbose=None):
		"""
		Requests the lowest offer listings for the specified marketplace
		products.

		*marketplace_id* (``str``) is the ID of the Amazon Marketplace the
		products belong to.

		*id_type* (``str``) is the type of ID used. This can only be
		"ASIN" or "SellerSKU".

		*id_list* (**sequence**) contains the ID (``str``) of each product
		to get. A maximum of 20 IDs can be requested at a single time.

		*condition* (``str``) optionally filters the returned listings to be
		based upon item condition. This can be any key or value from
		``ITEM_CONDITIONS``. Default is ``None`` for no filter.

		*exclude_me* (``bool``) optionally filters out listings that belong
		to the seller from the returned listings. This is only valid when
		*id_type* is "SellerSKU". Default is ``None`` for no filter.

		Returns the response XML (``str``).
		"""
		if not isinstance(marketplace_id, six.string_types):
			raise TypeError("marketplace_id:{!r} is not a str.".format(marketplace_id))
		elif not marketplace_id:
			raise ValueError("marketplace_id:{!r} cannot be empty.".format(marketplace_id))

		if not isinstance(id_type, six.string_types):
			raise TypeError("id_type:{!r} is not a str.".format(id_type))
		elif not id_type:
			raise ValueError("id_type:{!r} cannot be empty.".format(id_type))

		if not is_sequence(id_list):
			raise TypeError("id_list:{!r} is not a sequence.".format(id_list))
		elif not id_list:
			raise ValueError("id_list:{!r} cannot be empty.".format(id_list))
		elif len(id_list) > 20:
			raise ValueError("id_list length:{} cannot be greater than 20.".format(len(id_list)))

		if condition is not None:
			condition = ITEM_CONDITIONS.get(condition, condition)
			if not isinstance(condition, six.string_types):
				raise TypeError("condition:{!r} is not a str.".format(condition))
			elif not condition:
				raise ValueError("condition:{!r} cannot be empty.".format(condition))

		args = self.new_args()
		args['IdType'] = id_type
		if id_type == 'ASIN':
			if exclude_me is not None:
				raise ValueError("exclude_me:{!r} can only be set when id_type:{!r} is 'SellerSKU'.".format(exclude_me, id_type))
			args['Action'] = ACTIONS['get_lowest_listing_for_asin']
			args.update({'ASINList.ASIN.{}'.format(i): asin for i, asin in enumerate(id_list, 1)})
		elif id_type == 'SellerSKU':
			if exclude_me is not None:
				args['ExcludeMe'] = 'true' if exclude_me else 'false'
			args['Actions'] = ACTIONS['get_lowest_listing_for_sku']
			args.update({'SellerSKUList.SellerSKU.{}'.format(i): sku for i, sku in enumerate(id_list, 1)})
		else:
			raise ValueError("id_type:{!r} is not 'ASIN' or 'SellerSKU'.".format(id_type))
		if condition is not None:
			args['ItemCondition'] = condition

		return self.send_request(args, path=self.path, verbose=verbose)

	def get_products(self, marketplace_id, id_type, id_list, verbose=None):
		"""
		Requests the information for the specified marketplace products.

		*marketplace_id* (``str``) is the ID of the Amazon Marketplace the
		products are coming from.

		*id_type* (``str``) is the type of ID used. This can be only of the
		types listed under ``ID_TYPES``.

		*id_list* (**sequence**) contains the ID (``str``) of each product
		to get. A maximum of 5 IDs can be requested at a single time.

		Returns the response XML (``str``).
		"""
		if not isinstance(marketplace_id, six.string_types):
			raise TypeError("marketplace_id:{!r} is not a str.".format(marketplace_id))
		elif not marketplace_id:
			raise ValueError("marketplace_id:{!r} cannot be empty.".format(marketplace_id))

		if not isinstance(id_type, six.string_types):
			raise TypeError("id_type:{!r} is not a str.".format(id_type))
		elif not id_type:
			raise ValueError("id_type:{!r} cannot be empty.".format(id_type))

		if not is_sequence(id_list):
			raise TypeError("id_list:{!r} is not a sequence.".format(id_list))
		elif not id_list:
			raise ValueError("id_list:{!r} cannot be empty.".format(id_list))

		if len(id_list) > 5:
			raise ValueError("id_list length:{} cannot be greater than 5.".format(len(id_list)))

		args = self.new_args()
		args['IdType'] = id_type
		args['Action'] = ACTIONS['get_products_for_id']
		args.update({'IDList.ID.{}'.format(i): id_ for i, id_ in enumerate(id_list, 1)})

		return self.send_request(args, path=self.path, verbose=verbose)

	def get_my_price(self, marketplace_id, id_type, id_list, condition=None, verbose=None):
		"""
		Requests the seller's price for the specified marketplace products.

		*marketplace_id* (``str``) is the ID of the Amazon Marketplace the
		products belong to.

		*id_type* (``str``) is the type of ID used. This can only be
		"ASIN" or "SellerSKU".

		*id_list* (**sequence**) contains the ID (``str``) of each product
		to get. A maximum of 20 IDs can be requested at a single time.

		*condition* (``str``) optionally filters the returned listings to be
		based upon item condition. This can be any key or value from
		``ITEM_CONDITIONS``. Default is ``None`` for no filter.

		Returns the response XML (``str``).
		"""
		if not isinstance(marketplace_id, six.string_types):
			raise TypeError("marketplace_id:{!r} is not a str.".format(marketplace_id))
		elif not marketplace_id:
			raise ValueError("marketplace_id:{!r} cannot be empty.".format(marketplace_id))

		if not isinstance(id_type, six.string_types):
			raise TypeError("id_type:{!r} is not a str.".format(id_type))
		elif not id_type:
			raise ValueError("id_type:{!r} cannot be empty.".format(id_type))

		if not is_sequence(id_list):
			raise TypeError("id_list:{!r} is not a sequence.".format(id_list))
		elif not id_list:
			raise ValueError("id_list:{!r} cannot be empty.".format(id_list))
		elif len(id_list) > 20:
			raise ValueError("id_list length:{} cannot be greater than 20.".format(len(id_list)))

		if condition is not None:
			condition = ITEM_CONDITIONS.get(condition, condition)
			if not isinstance(condition, six.string_types):
				raise TypeError("condition:{!r} is not a str.".format(condition))
			elif not condition:
				raise ValueError("condition:{!r} cannot be empty.".format(condition))

		args = self.new_args()
		args['IdType'] = id_type
		if id_type == 'ASIN':
			args['Action'] = ACTIONS['get_my_price_for_asin']
			args.update({'ASINList.ASIN.{}'.format(i): asin for i, asin in enumerate(id_list, 1)})
		elif id_type == 'SellerSKU':
			args['Actions'] = ACTIONS['get_my_price_for_sku']
			args.update({'SellerSKUList.SellerSKU.{}'.format(i): sku for i, sku in enumerate(id_list, 1)})
		else:
			raise ValueError("id_type:{!r} is not 'ASIN' or 'SellerSKU'.".format(id_type))
		if condition is not None:
			args['ItemCondition'] = condition

		return self.send_request(args, path=self.path, verbose=verbose)

	def list_matching(self, marketplace_id, query, context, verbose=None):
		"""
		Requests the marketplace products that match the query.

		*marketplace_id* (``str``) is the ID of the Amazon Marketplace to
		list the products from.

		*query* (``str``) is a basic search string. No special functionality
		is supported by Amazon for the search query beyond *context*.

		*context* (``str``) is the query context. This is basically the
		generic category to search under. This can be any key or value from
		``QUERY_CONTEXTS``.

		Returns the response XML (``str``).
		"""
		if not isinstance(marketplace_id, six.string_types):
			raise TypeError("marketplace_id:{!r} is not a str.".format(marketplace_id))
		elif not marketplace_id:
			raise ValueError("marketplace_id:{!r} cannot be empty.".format(marketplace_id))

		if not isinstance(query, six.string_types):
			raise TypeError("query:{!r} is not a str.".format(query))
		elif not query:
			raise ValueError("query:{!r} cannot be empty.".format(query))

		if context is not None:
			context = QUERY_CONTEXTS.get(context, context)
			if not isinstance(context, six.string_types):
				raise TypeError("context:{!r} is not a str.".format(context))
			elif not context:
				raise ValueError("context:{!r} cannot be empty.".format(context))

		args = self.new_args()
		args['Action'] = ACTIONS['list_matching']
		args['MarketplaceId'] = marketplace_id
		args['Query'] = query
		if context is not None:
			args['QueryContextId'] = context

		return self.send_request(args, path=self.path, verbose=verbose)

	def new_args(self):
		"""
		Returns a new ``dict`` of default arguments.
		"""
		return {
			'AWSAccessKeyId': self.access_key,
			'SellerId': self.merchant_id,
			'Timestamp': datetime_to_iso8601(datetime.datetime.utcnow()),
			'Version': self.products_api_version
		}
