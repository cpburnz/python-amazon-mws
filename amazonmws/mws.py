# coding: utf-8
"""
This module provides the base implementation of the Amazon MWS API for
authenticating, sending and receiving requests.
"""

__author__ = "Caleb P. Burns"
__created__ = "2012-11-20"
__modified__ = "2016-03-29"
__modified_by___ = "Joshua D. Burns"

import six # Python2/Python3 compatibility library.
import base64
import hashlib
import hmac
import os.path
import platform
import pprint
import re
import sys
import urllib

from amazonmws import __version__
from amazonmws.util import is_sequence

#: MWS API Endpoints
ENDPOINTS = {
	'ca': 'https://mws.amazonservices.ca',     # Canada
	'cn': 'https://mws.amazonservices.com.cn', # China
	'eu': 'https://mws-eu.amazonservices.com', # Europe (Germany, Spain, France, Italy, United Kingdom)
	'in': 'https://mws.amazonservices.in',     # India
	'jp': 'https://mws.amazonservices.jp',     # Japan
	'us': 'https://mws.amazonservices.com',    # United States
}

#: Marketplace IDs
MARKETPLACE_IDS = {
	'ca': 'A2EUQ1WTGCTBG2', # Canada
	'cn': 'AAHKV2X7AFYLW',  # China
	'in': 'A21TJRUUN4KGV',  # India
	'jp': 'A1VC38T7YXB528', # Japan
	'us': 'ATVPDKIKX0DER',  # United States
	# Europe
	'de': 'A1PA6795UKMFR9', # Germany
	'es': 'A1RKKUPIHCS9HS', # Spain
	'fr': 'A13V1IB3VIYZZH', # France
	'it': 'APJ6JRA9NG5V4',  # Italy
	'uk': 'A1F83G8C2ARO7P', # United Kingdom
}

#: Envelope message types.
MESSAGE_TYPES = {
	'cat_pil': 'CatPIL',
	'character_data': 'CharacterData',
	'customer': 'Customer',
	'fulfillment_center': 'FulfillmentCenter',
	'fulfillment_order_cancellation_request': 'FulfillmentOrderCancellationRequest',
	'fulfillment_order_request': 'FulfillmentOrderRequest',
	'image': 'Image',
	'inventory': 'Inventory',
	'invoice_confirmation': 'InvoiceConfirmation',
	'item': 'Item',
	'listings': 'Listings',
	'loyalty': 'Loyalty',
	'multi_channel_order_report': 'MultiChannelOrderReport',
	'navigation_report': 'NavigationReport',
	'offer': 'Offer',
	'order_acknowledgement': 'OrderAchnowledgement',
	'order_adjustment': 'OrderAdjustment',
	'order_fulfillment': 'OrderFulfillment',
	'order_notification_report': 'OrderNotificationReport',
	'order_report': 'OrderReport',
	'override': 'Override',
	'price': 'Price',
	'processing_report': 'ProcessingReport',
	'product': 'Product',
	'product_image': 'ProductImage',
	'relationship': 'Relationship',
	'reverse_item': 'ReverseItem',
	'store': 'Store',
	'webstore_item': 'WebstoreItem',
	'pending_order_report': 'PendingOrderReport'
}

#: Operation types.
OPERATION_TYPES = {
	'delete': 'Delete',
	'update': 'Update',
	'partial_update': 'PartialUpdate'
}

#: Carrier codes.
CARRIER_CODES = {
	'blue_package': 'Blue Package',
	'canada_post': 'Canada Post',
	'city_link': 'City Link',
	'dhl': 'DHL',
	'dhl_global': 'DHL Global Mail',
	'fastway': 'Fastway',
	'fedex': 'FedEx',
	'fedex_smart_post': 'FedEx SmartPost',
	'gls': 'GLS',
	'go': 'GO!',
	'hermes_logistik_gruppe': 'Hermes Logistik Gruppe',
	'newgistics': 'Newgistics',
	'nippon_express': 'NipponExpress',
	'on_trac': 'OnTrac',
	'osm': 'OSM',
	'parcelforce': 'Parcelforce',
	'royal_mail': 'Royal Mail',
	'sagawa_express': 'SagawaExpress',
	'streamlite': 'Streamlite',
	'target': 'Target',
	'tnt': 'TNT',
	'usps': 'USPS',
	'ups': 'UPS',
	'ups_mail_innovations': 'UPS Mail Innovations',
	'yamato_transport': 'YamatoTransport'
}

#: Currency codes.
CURRENCY_CODES = {
	'ca': 'CAD', # Canadian dollar
	'eu': 'EUR', # Euro
	'jp': 'JPY', # Japanese yen
	'gb': 'GBP', # British pound sterling
	'us': 'USD'  # Unites states dollar
}

#: Language types.
LANGUAGE_TYPES = {
	('en', 'ca'): 'en_CA',
	('en', 'gb'): 'en_GB',
	('en', 'us'): 'en_US',
	('fr', 'ca'): 'fr_CA',
	('fr', 'fr'): 'fr_FR',
	('de', 'de'): 'de_DE',
	('ja', 'jp'): 'ja_JP'
}

#: Signature methods.
SIGNATURE_METHODS = {
	'hmac_sha1': 'HmacSHA1',
	'hmac_sha256': 'HmacSHA256'
}


class MWS(object):
	"""
	The ``MWS`` class is the base class used to interact with the Amazon
	MWS API. This class implements authentication, sending and receiving
	requests.
	"""

	app_name = "PythonAmazonMWS"
	"""
	*app_name* (``str``) is the name of this API.
	"""

	app_version = __version__
	"""
	*app_version* (``str``) is the version of this API.
	"""

	client_api_version = None
	"""
	*client_api_version* (``str``) is the version of the client API. This
	should be set by subclasses to indicate the version of their
	respective API.
	"""

	ua_enc = 'UTF-8'
	"""
	*ua_enc* (``str``) is the encoding the user agent string will be
	encoded as.
	"""

	ua_escape_re = re.compile(r"([\/(=);])")
	"""
	*ua_escape_re* (``re.RegexObject``) is used by *ua_escape()* to match
	characters which need to be escaped.
	"""

	ua_escape_repl = r"\\\1"
	"""
	*ua_escape_repl* (``str``) is used by *ua_escape()* to escape matched
	characters.
	"""

	max_size = 2**31 - 1
	"""
	*max_size* (``int``) is the maximum size a request body can be.
	"""

	def __init__(self, access_key, secret_key, merchant_id, endpoint, agent=None, user_agent=None):
		"""
		Initializes an ``MWS`` instance.

		*access_key* (``str``) is your Amazon supplied AWS Access Key ID.

		*secret_key* (``str``) is your Amazon supplied AWS Secret Access Key
		used to sign requests.

		*merchant_id* (``str``) is your Amazon supplied Merchant ID.

		*endpoint* (``str``) is the Amazon Endpoint Server. This can be
		either the actual endpoint URL or a key from ``ENDPOINTS``.

		*agent* (``MWSAgent``) optionally is the agent to use which actually
		sends the requests. Default is ``None`` to use a new ``MWSAgent``
		instance.

		*user_agent* (``str``) optionally is the user agent string to use.
		Default is ``None`` to use the one generated by *self.ua_new()*.
		"""

		self.access_key = None
		"""
		*access_key* (``str``) is your Amazon supplised Access Key.
		"""

		self.agent = None
		"""
		*agent* (``MWSAgent``) is the agent used to actually send the
		requests.
		"""

		self.endpoint = None
		"""
		*endpoint* (``str``) is the Amazon MWS Endpoint Server.
		"""

		self.merchant_id = None
		"""
		*merchant_id* (``str``) is your Amazon supplised Merchant ID.
		"""

		self.user_agent = None
		"""
		*user_agent* (``str``) is the user agent string to use for requests.
		"""

		self.secret_key = None
		"""
		*secret_key* (``str``) is used the secret key used sign requests.
		"""

		if not isinstance(access_key, six.string_types):
			raise TypeError("access_key:{!r} must be a string.".format(access_key))
		elif not access_key:
			raise ValueError("access_key:{!r} cannot be empty.".format(access_key))
		access_key = str(access_key)

		if not isinstance(secret_key, six.string_types):
			raise TypeError("secret_key:{!r} must be a string.".format(secret_key))
		elif not secret_key:
			raise ValueError("secret_key:{!r} cannot be empty.".format(secret_key))
		secret_key = str(secret_key)

		endpoint = ENDPOINTS.get(endpoint, endpoint)
		if not isinstance(endpoint, six.string_types):
			raise TypeError("endpoint:{!r} must be a string.".format(endpoint))
		elif not endpoint:
			raise ValueError("endpoint:{!r} cannot be empty.".format(endpoint))
		endpoint = str(endpoint)

		if not isinstance(merchant_id, six.string_types):
			raise TypeError("merchant_id:{!r} must be a string.".format(merchant_id))
		elif not merchant_id:
			raise ValueError("merchant_id:{!r} cannot be empty.".format(merchant_id))
		merchant_id = str(merchant_id)

		if agent is not None and not isinstance(agent, IMWSAgent):
			raise TypeError("agent:{!r} is not an IMWSAgent.".format(agent))

		if user_agent is not None:
			if not isinstance(user_agent, six.string_types):
				raise TypeError("user_agent:{!r} must be a string or None.".format(user_agent))
			elif not user_agent:
				raise ValueError("user_agent:{!r} cannot be empty.".format(user_agent))

		self.access_key = access_key
		self.secret_key = secret_key
		self.merchant_id = merchant_id
		self.endpoint = endpoint

		self.agent = agent or MWSAgent()

		#self.user_agent = six.u(user_agent or self.ua_new(self.client_api_version, self.app_name, self.app_version)).encode(self.ua_enc)
		self.user_agent = user_agent or self.ua_new(self.client_api_version, self.app_name, self.app_version)

	def send_request(self, args, body=None, content_type=None, path=None, debug=None):
		"""
		Sends the request to MWS.

		*args* are query parameters to send as part of the request. This can
		be either a ``dict`` mapping *key* to *value* or a **sequence** of
		*key*-*value* 2-``tuple`` pairs. The "Action" key must be set, and
		the "Signature", "SignatureMethod" and "SignatureVersion" keys must
		not be set.

		- *key* (``str``) is the argument key.

		- *value* is the argument value which can be either a single value
		  (``str``) or a **sequence** containing each value (``str``). If a
		  **sequence**, *key* will be repeated for each value.

		*body* (``str`` or ``file``) optionally is the request body to send.
		This can be either the body bytes (``str``) or a ``file`` supporting
		``read()`` (``seek()`` and ``tell()`` are optional). Default is
		``None`` for no body.

		.. NOTE:: If a ``file``, it will not be closed (i.e., you are still
		   responsible for calling ``close()`` on it).

		*content_type* (``str``) is the content type of *body*. This must be
		set if *body* is set. If passing a Feed Type of XML, you will most
		likely want to set this to "text/XML". If feeding a Flat File,
		you'll need to specify one of the following, based on marketplace:
		- North America and Europe (US, France, Germany, Italy, Spain, UK):
			"text/tab-separated-values; charset=iso-8859-1"
		- Japan: "text/tab-separated-values; charset=Shift_JIS"
		- China: "text/tab-separated-values;charset=UTF-8"
		           OR ...
		         "text/tab-separated-values;charset=UTF-16"
		Default is ``None`` because *body* is ``None``.

		*path* (``str``) is the URL path to request. Default is ``None`` for
		"/". This is "/" for most of the Amazon MWS API.

		*debug* (``dict``) is whether debugging information should be
		printed. Default is ``None`` for no debugging.

		Returns the response which is dependent upon *self.agent*. The
		default *agent* returns the response body (``str``).
		"""
		return self.agent.request(self, path, args, body, content_type, debug=debug)

	def ua_escape(self, value):
		"""
		Escapes a user agent value.

		*value* (**string**) is the value to escape.

		Returns the escaped value (**string**).
		"""
		return self.ua_escape_re.sub(self.ua_escape_repl, value)

	def ua_new(self, client, app, version):
		"""
		Generates a new user agent string.

		*client* (**string**) is the MWS client version.

		*app* (**string**) is the name of the application.

		*version* (``str``) is the version of the application.

		Returns the user agent string (**string**).
		"""
		attrs = []

		lang = "Language={python}/{version}".format(
			python=self.ua_escape(platform.python_implementation()),
			version=self.ua_escape(platform.python_version())
		)
		attrs.append(lang)

		plat = "Platform={system}/{machine}/{release}".format(
			system=self.ua_escape(platform.system()),
			machine=self.ua_escape(platform.machine()),
			release=self.ua_escape(platform.release())
		)
		attrs.append(plat)

		if client:
			client = "MWSClientVersion={version}".format(
				version=self.ua_escape(client)
			)
			attrs.append(client)

		user_agent = u"{app}/{version}".format(
			app=self.ua_escape(app),
			version=self.ua_escape(version)
		)
		if attrs:
			user_agent += " ({attrs})".format(attrs="; ".join(attrs))

		return user_agent


class IMWSAgent(object):
	"""
	The ``IMWSAgent`` class is the interface that all MWS Agent classes
	must implement. The Agent is what actually sends requests to Amazon.
	"""

	def request(self, mws, path, args, body, content_type, debug=None):
		"""
		Perform the request.

		*mws* (``MWS``) is the MWS instance.

		*path* (``str``) is the request path.

		*args* contains the query parameters.

		*body* (``str`` or ``file``) contains the body of the request.

		*content_type* (``str``) is the content type of *body*.

		*debug* (``dict``) optionally is whether debugging information
		should be printed. Default is ``None`` for no debugging.

		Returns the response body (``str``).

		.. NOTE:: Subclasses must override this.
		"""
		raise NotImplementedError("Subclasses must implement request() without calling IMWSAgent.request().")


class MWSAgent(IMWSAgent):
	"""
	The ``MWSAgent`` class is the default implementation of the
	``IMWSAgent`` class used by the ``MWS`` class. This implementation
	does everything blocking, inline and synchronously.
	"""

	req_args_required = {'Action'}
	"""
	*req_args_required* (``set``) contains the required request arguments.
	"""

	req_args_safe_chars = "~"
	"""
	*req_args_safe_chars* (``str``) contains additional charaters that do
	not need to be escaped in arguments. This is passed to ``urllib.quote_plus()``.
	"""

	req_args_sig = {'Signature', 'SignatureMethod', 'SignatureVersion'}
	"""
	*req_args_sig* (``set``) contains the request arguments used by the
	signature.
	"""

	sig_version = 2
	"""
	*sig_version* (``int``) is the signature version used by *self.sign_request()*.
	"""

	sig_method = 'hmac_sha256'
	"""
	*sig_method* (``str``) is the HMAC hash algorithm used to calculate
	the signature by *self.sign_request()*.
	"""

	sort_args_re = re.compile(r"(\d+|\D+)")
	"""
	*sort_args_re* (``re.RegexObject``) is used by *self.sort_args_key()*
	to natural sort args.
	"""

	def build_request(self, mws, path, args, body, content_type, debug=None):
		"""
		Builds the request.

		.. NOTE:: This should not be called directly. Use *self.request()*.

		*mws* (``MWS``) is the MWS instance.

		*path* (``str``) is the request path.

		*args* contains the query parameters.

		*body* (``str`` or ``file``) contains the body of the request. This
		can be ``None``.

		*content_type* (``str``) is the content type of *body*.

		*debug* (``dict``) is whether debugging information should be
		printed. Default is ``None`` for no debugging.

		- *body* (``bool``) is whether the request body should be printed
		  (``True``), or not (``False``). Default is ``None`` for ``False``.

		- *info* (``bool``) is whether the request args and headers should
		  be printed (``True``), or not (``False``).

		- *url* (``bool``) is whether the generated URL should be printed
		  (``True``), or not (``False``). Default is ``None`` for ``False``.

		Returns a ``tuple`` containing: *method*, the request URL (``str``),
		the request headers (``dict`` or ``None``), and the request body
		(``str``, ``file`` or ``None``).
		"""
		if debug is None:
			debug = {}

		if not isinstance(mws, MWS):
			raise TypeError("mws:{!r} is not an MWS.".format(mws))

		if isinstance(args, dict):
			args = list(six.iteritems(args))
		elif is_sequence(args):
			args = args[:]
		else:
			raise TypeError("args:{!r} must be a dict or sequence.".format(args))

		# Check for missing and reserved args.
		arg_keys = set([k for k, _v in args])
		missing = self.req_args_required - arg_keys
		if len(missing) > 1:
			raise KeyError("args:{!r} is missing keys: {}.".format(args, ", ".join(map(repr, missing))))
		elif missing:
			raise KeyError("args:{!r} is missing key: {!r}.".format(args, missing.pop()))
		reserved = self.req_args_sig & arg_keys
		if len(reserved) > 1:
			raise KeyError("args:{!r} cannot have keys: {}.".format(args, ", ".join(map(repr, reserved))))
		elif reserved:
			raise KeyError("args:{!r} cannot have key: {!r}.".format(args, reserved.pop()))

		if body is not None:
			if isinstance(body, six.string_types):
				# Ensure string types are byte-arrays.
				body = six.b(body)
			body_is_str = isinstance(body, six.binary_type)
			body_is_file = callable(getattr(body, 'read', None))
			if not body_is_str and not body_is_file:
				raise TypeError("body:{!r} is not a str or file.".format(body))

			if not isinstance(content_type, six.string_types):
				raise TypeError("content_type:{!r} is not a str.".format(content_type))
			elif not content_type:
				raise ValueError("content_type:{!r} cannot be empty.".format(content_type))

		if path is not None and not isinstance(path, six.string_types):
			raise TypeError("path:{!r} is not a str.".format(path))

		# Query.
		args += [
			('SignatureMethod', SIGNATURE_METHODS[self.sig_method]),
			('SignatureVersion', self.sig_version)
		]
		args = sorted(args, key=self.sort_args_key)
		query = "&".join((
			"{}={}".format(six.moves.urllib.parse.quote(str(k), self.req_args_safe_chars), six.moves.urllib.parse.quote(str(v), self.req_args_safe_chars))
		) for k, vals in args for v in (vals if is_sequence(vals) else [vals]))

		# Signature
		method = "GET" if body is None else "POST"
		result = six.moves.urllib.parse.urlparse(mws.endpoint)
		domain = result.netloc or result.path
		path = six.moves.urllib.parse.quote(os.path.normpath('/' + path.lstrip('/'))) if path else "/"
		sig = self.sign_request(mws.secret_key, method, domain, path, query)

		# URL.
		url = "{host}{path}?{query}&Signature={sig}".format(
			host=mws.endpoint,
			path=path,
			query=query,
			sig=six.moves.urllib.parse.quote(sig, safe='/')
		)

		# Headers.
		headers = {
			'User-Agent': mws.user_agent
		}

		if body is not None:
			if body_is_str:
				body_len = len(body)
				body_md5 = base64.b64encode(hashlib.md5(body).digest())
			elif body_is_file:
				if callable(getattr(body, 'seek', None)) and callable(getattr(body, 'tell', None)):
					# MD5 body and get length.
					pos = body.tell()
					md5 = hashlib.md5()
					while True:
						chunk = body.read(2**16)
						if not chunk:
							break
						md5.update(chunk)
					body_len = body.tell() - pos
					body_md5 = base64.b64encode(md5.digest())
					body.seek(pos, os.SEEK_SET)

				else:
					body = body.read()
					body_len = len(body)
					body_md5 = base64.b64encode(hashlib.md5(body).digest())
					body_is_file = False

			if body_len > mws.max_size:
				raise ValueError("body length:{!r} cannot be greater than {}.".format(body_len, mws.max_size))

			headers['Content-Type'] = content_type
			headers['Content-Length'] = body_len
			headers['Content-MD5'] = body_md5

		# Debug info.
		if debug:
			if debug.get('url', False):
				print("URL ({}:{})".format(url.__class__.__name__, len(url)))
				print("--------")
				print(url)
				print("--------")
			if debug.get('info', False):
				print("Args ({})".format(len(args)))
				print("---------")
				pprint.pprint(args)
				print("---------")
				print("Headers ({})".format(len(headers)))
				print("------------")
				pprint.pprint(headers)
				print("------------")
			if debug.get('body', False) or debug.get('info', False):
				print("Body ({}:{})".format(body.__class__.__name__, body_len))
			if debug.get('body', False):
				print("-"*20)
				if body_is_file:
					pos = body.tell()
					print(body.read())
					body.seek(pos, os.SEEK_SET)
				else:
					print(body)
				print("-"*20)

		return method, url, headers, body

	def request(self, mws, path, args, body, content_type, debug=None):
		"""
		Perform the request.

		*mws* (``MWS``) is the MWS instance.

		*path* (``str``) is the request path.

		*args* contains the query parameters.

		*body* (``str`` or ``file``) contains the body of the request. This
		can be ``None``.

		*content_type* (``str``) is the content type of *body*.

		*debug* (``dict``) is whether debugging information should be
		printed. Default is ``None`` for no debugging.

		Returns the response body (``str``).
		"""
		method, url, headers, body = self.build_request(mws, path, args, body, content_type, debug=debug)
		return self.send_request(method, url, headers, body, debug=debug)

	def send_request(self, method, url, headers, body, debug=None):
		"""
		Send the request.

		.. NOTE:: This should not be called directly. Use *self.request()*.

		*method* (``str``) is the HTTP request method.

		*url* (``str``) is the URL of the request.

		*headers* (``dict``) are any headers to send. This can be ``None``.

		*body* (``str`` or ``file``) is the body of the request. This can be
		``None``.

		*debug* (``dict``) is whether debugging information should be
		printed. Default is ``None`` for no debugging.

		Returns the response body (``str``).
		"""
		if callable(getattr(body, 'read', None)):
			body = body.read()
		request = six.moves.urllib.request.Request(url, data=body, headers=headers)
		try:
			response = six.moves.urllib.request.urlopen(request, timeout=30)
			data = response.read()
		except six.moves.urllib.error.HTTPError as e:
			data = e.read()
			if not data:
				raise
		return data

	def sign_request(self, key, method, domain, path, query):
		"""
		Generates the request signature.

		*key* (``MWS``) is the secret key used to sign the request.

		*method* (``str``) is the HTTP method: "GET" or "POST".

		*domain* (``str``) is the request domain.

		*path* (``str``) is the request URL path.

		*query* (``str``) is the request URL query parameters.

		Returns the request signature base64 encoded (``str``).
		"""
		if self.sig_version != 2:
			raise SignatureError("Only signature version 2 is supported, not {!r}.".format(self.sig_version))

		# Create data.
		data = "{method}\n{domain}\n{path}\n{query}".format(
			method=method.upper(),
			domain=domain.lower(),
			path=path,
			query=query
		)

		# Hash data.
		hmac_func = getattr(self, 'sign_' + self.sig_method, None)
		if not callable(hmac_func):
			raise SignatureError("Signature method {!r} is not supported.".format(self.sig_method))
		sig = hmac_func(key, data)

		# Returned encoded hash.
		return base64.b64encode(sig)

	def sign_hmac_sha1(self, key, data):
		"""
		Signs the request using HMAC SHA1.

		*key* (``str``) is the secret key used to sign *data*.

		*data* (``str``) is the request data to sign.

		Returns the data signature (``str``).
		"""
		return hmac.new(key, data, hashlib.sha1).digest()

	def sign_hmac_sha256(self, key, data):
		"""
		Signs the request using HMAC SHA256.

		*key* (``str``) is the secret key used to sign *data*.

		*data* (``str``) is the request data to sign.

		Returns the data signature (``str``).
		"""
		return hmac.new(six.b(key), six.b(data), hashlib.sha256).digest()

	def sort_args_key(self, key):
		"""

		NOTE: This method is deprecated. Amazon MWS expects sorting in
		      natural BYTE ORDER, not natural-order. By sorting by
		      natural order, when IDs over a value of 9 are encountered,
			MWS complains about a bad signature.

		This is used by *self.build_request()* to sort arguments. This
		implementation performs a natural sort so that when query arguments
		named in the style "{full_name}.{short_name}.{n}" are ordered
		properly for when the signature is genereted.

		*key* (``str``) is the key.

		Returns the key (``object``) to use to sort by.
		"""
		return key

		# If sending more than 10 Report IDs to
		# UpdateReportAcknowledgements, Amazon MWS gives an error stating
		# that the signature does not match. If sending 9, it works just
		# fine. We have deducted that Amazon is not performing a natural
		# sort on at *least* UpdateReportAcknowledgements Report IDs.
		# We need to test other methods which support more than 10 IDs being
		# passed to determine if this is a Call-specific limitation, or if
		# across the board all sorting should be done the default "python"
		# way.
		#return [int(s) if s.isdigit() else s for s in self.sort_args_re.findall(key[0])] # Natural sort


class SignatureError(Exception):
	"""
	The `SignatureError` exception is raised when there is an error
	generating the signature for a request.
	"""
