# coding: utf-8
# pylint: disable=C0103
"""
This module contains helpers to support using the Amazon MWS API from
Twisted.

.. NOTE:: The ``MWSAgent`` defined in this module is not working with Amazon.
   I get an SSL timeout whenever I try using this class to submit a request.
"""
from __future__ import absolute_import

__created__ = "2012-12-31"
__modified__ = "2013-03-28"

from cStringIO import StringIO

import twisted.internet.defer as defer
import twisted.internet.protocol as protocol
import twisted.internet.reactor as reactor
import twisted.internet.threads as threads
import twisted.web.client as client
import twisted.web.http as http
from twisted.web.http_headers import Headers

import amazonmws.mws

class MWSAgent(amazonmws.mws.MWSAgent):
	"""
	The ``MWSAgent`` class is an alternate implementation of the
	``amazonmws.mws.IMWSAgent`` class. This implementation uses threads
	for blocking code, and ``twisted.web.client.Agent`` to asynchronously
	send requests.
	"""

	def __init__(self, pool=None):
		"""
		Initializes the ``MWSAgent`` instance.

		*pool* (``twisted.web.client.HTTPConnectionPool``) optionally is the
		connection pool to use. Default is ``None``.
		"""

		self.tx_agent = None
		"""
		*tx_agent* (``twisted.web.client.Agent``) is the Twisted Agent used
		to send requests.
		"""

		# Create twisted agent.
		self.tx_agent = client.Agent(reactor, pool=pool)

	@defer.inlineCallbacks
	def request(self, mws, path, args, body, content_type, verbose=None):
		"""
		Perform the request.

		*mws* (``MWS``) is the MWS instance.

		*path* (``str``) is the request path.

		*args* contains the query parameters.

		*body* (``str`` or ``file``) contains the body of the request.

		*content_type* (``str``) is the content type of *body*.

		*verbose* (``int``) optionally is whether verbose debugging
		information should be printed. Default is ``None`` for ``0``.

		Returns a deferred (``twisted.internet.defer.Deferred``) which is
		fired with the response body (``str``) once the request completes.
		"""
		# Build and send request.
		method, url, headers, body = yield threads.deferToThread(self.build_request, mws, path, args, body, content_type, verbose=verbose)


		print "BODY {} ({})".format(body, body.tell())
		print "-"*20
		pos = body.tell()
		print body.read()
		body.seek(pos, 0)
		print "-"*20


		response = yield self.send_request(method, url, headers, body)

		# Get and return response.
		response = Response(response)
		yield response.body
		defer.returnValue(response)


		# Get and return response.
		d = defer.Deferred()
		response.deliverBody(BodyReceiver(d))
		result = yield d
		defer.returnValue(result)

	def send_request(self, method, url, headers, body):
		"""
		Send the request.

		.. NOTE:: This should not be called directly. Use *self.request()*.

		*method* (``str``) is the HTTP request method.

		*url* (``str``) is the URL of the request.

		*headers* (``dict``) are any headers to send. This can be ``None``.

		*body* (``str`` or ``file``) is the body of the request. This can be
		``None``.

		Returns a deferred (``twisted.internet.defer.Deferred``) which is
		fired with the response (``twisted.web.iweb.IResponse``) once all
		response headers have been received.
		"""
		body_is_file = callable(getattr(body, 'read', None))
		headers = Headers({key: [val] for key, val in headers.iteritems()}) if headers else None
		#producer = FileBodyProducer(body if body_is_file else StringIO(body)) if body is not None else None
		producer = XXXStringProducer(body.read() if body_is_file else body) if body is not None else None
		return self.tx_agent.request(method, url, headers=headers, bodyProducer=producer)


class Response(object):

	def __init__(self, response):
		self.version = response.version
		self.code = response.code
		self.phrase = response.phrase
		self.headers = response.headers
		self.length = response.length

		self.body = defer.Deferred()
		self.body.addCallback(self._body_cb)
		response.deliverBody(BodyReceiver(self.body))


	def __str__(self):
		return str(self.body)

	def _body_cb(self, body):
		self.body = body
		return body


class XXXStringProducer(object):
	def __init__(self, body):
		self.body = body
		self.length = len(body)

	def startProducing(self, consumer):
		consumer.write(self.body)
		return defer.succeed(None)

	def pauseProducing(self):
		pass

	def resumeProducing(self):
		pass

	def stopProducing(self):
		pass


class FileBodyProducer(client.FileBodyProducer):
	"""
	The ``FileBodyProducer`` class is used to send the request body. This
	extends ``twisted.web.client.FileBodyProducer`` so that the file is
	not closed.
	"""

	def stopProducing(self):
		if self._task._completionState is None:
			# Only stop when we have not already been stopped. Twisted is
			# calling this twice for some odd reason.
			self._task.stop()


class BodyReceiver(protocol.Protocol):
	"""
	The ``BodyReceiver`` class is used to buffer the response body and
	fire a deferred once the body is fully received.
	"""

	def __init__(self, deferred):
		"""
		Instantiates the ``BodyReceiver`` instance.

		*deferred* (``twisted.internet.defer.Deferred``) will be fired with
		the response body (``str``) once it has been fully received.
		"""
		self.__buffer = StringIO()
		self.__deferred = deferred

	def connectionLost(self, reason):
		"""
		Called when the connection is lost.

		*reason* (``twisted.python.failure.Failure``) is the reason the
		connection was lost.
		"""
		buff, self.__buffer = self.__buffer, None
		d, self.__deferred = self.__deferred, None
		if reason.check(client.ResponseDone, http.PotentialDataLoss):
			d.callback(buff.getvalue())
		else:
			d.errback(reason)

	def dataReceived(self, data):
		"""
		Called when data is received.

		*data* (``str``) is the bytes received.
		"""
		self.__buffer.write(data)
