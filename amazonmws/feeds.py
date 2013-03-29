# coding: utf-8
"""
This package provides an implementation of the Amazon MWS Feeds API.
Subpackages are available that provide classes for creating several
feeds.
"""

__author__ = "Caleb P. Burns"
__created__ = "2012-11-26"
__modified__ = "2013-03-28"
__status__ = "Development"

import datetime

import amazonmws.mws
from amazonmws.util import datetime_to_iso8601, encode_string, is_sequence, marketplace_args

#: Feed types.
FEED_TYPES = {
	'product_data': '_POST_PRODUCT_DATA_',
	'product_image': '_POST_PRODUCT_IMAGE_DATA_',
	'product_item': '_POST_ITEM_DATA_',
	'product_inventory': '_POST_INVENTORY_AVAILABILITY_DATA_',
	'product_pricing': '_POST_PRODUCT_PRICING_DATA_',
	'product_relationship': '_POST_PRODUCT_RELATIONSHIP_DATA_',
	'order_acknowledgement': '_POST_ORDER_ACKNOWLEDGEMENT_DATA_',
	'order_fulfillment': '_POST_ORDER_FULFILLMENT_DATA_'
}

#: Processing statuses..
PROCESSING_STATUSES = {
	'cancelled': '_CANCELLED_',
	'done': '_DONE_',
	'in_progress': '_IN_PROGRESS_',
	'submitted': '_SUBMITTED_'
}


class MWSFeeds(amazonmws.mws.MWS):
	"""
	The ``MWSFeeds`` class is used to send requests to the Amazon MWS
	Feeds API. The primary purpose of this class is to submit feeds to
	MWS and get the results back.
	"""

	client_api_version = __modified__
	"""
	*client_api_version* (``str``) is the version of this client API.
	"""

	feeds_api_version = '2009-01-01'
	"""
	*feeds_api_version* (``str``) is the version of the MWS Feeds API
	implemented.
	"""

	def new_args(self):
		"""
		Returns a new ``dict`` of default arguments.
		"""
		args = {
			'AWSAccessKeyId': self.access_key,
			'Merchant': self.merchant_id,
			'Timestamp': datetime_to_iso8601(datetime.datetime.utcnow()),
			'Version': self.feeds_api_version
		}
		return args

	def cancel_submissions(self, submissions=None, feed_types=None, from_date=None, to_date=None, all_submissions=None, debug=None):
		"""
		Requests all Feed Submissions that match the specified criteria to
		be cancelled.

		.. NOTE:: Only feeds that have been submitted but have not yet been
		   processed can be cancelled (i.e., where status is "_SUBMITTED_").

		To delete specific Feed Submissions, set *submissions*:

		*submissions* (**sequence**) contains the ID (``str``) of each Feed
		Submission to cancel.

		To delete Feed Submissions based upon a query, use any of the
		following: *feed_types*, *from_date*, *to_date*.

		*feed_types* (**sequence**) contains each Feed Type (``str``) to
		filter the list of submissions to cancel. This can contain any of
		the keys and values from ``FEED_TYPES``. Default is ``None`` for all
		Feed Types.

		*from_date* (``datetime.datetime`` or ``float``) is the earliest
		date to filter the list of submissions to cancel. Default is
		``None`` for 180 days ago.

		*to_date* (``datetime.datetime`` or ``float``) is the latest date to
		filter the list of submissions to cancel. Default is ``None`` for
		now.

		To delete all Feed Submissions, set *all_submissions* to ``True``:

		*all_submissions* (``bool``) indicates whether all Feed Submissions
		should be deleted (``True``), or not (``False``). This is used to
		prevent accidental deletion of all Feed Submissions.

		Returns the response XML (``str``).
		"""
		cancel_list = 1 if submissions is not None else 0
		cancel_query = 1 if (feed_types is not None or from_date is not None or to_date is not None) else 0
		cancel_all = 1 if all_submissions else 0
		cancel_sum = cancel_list + cancel_query + cancel_all
		if cancel_sum != 1:
			if cancel_sum:
				msg = []
				if cancel_list:
					msg.append("submissions:{subs!r}")
				if cancel_query:
					msg.append("a query (feed_types:{types!r}, from_date:{from_date!r}, and to_date:{to_date!r})")
				if cancel_all:
					msg.append("all_submissions:{all_subs!r}")
				msg = "Only one of {} can be set.".format(", or ".join(msg))
			else:
				msg = "Either submissions:{subs!r}, or a query (feed_types:{types!r}, from_date:{from_date!r}, and to_date:{to_date!r}), or all_submissions:{all_subs!r} must be set."

			raise ValueError(msg.format(subs=submissions, types=feed_types, to_date=to_date, from_date=from_date, all_subs=all_submissions))

		# Build args.
		args = self.new_args()
		args['Action'] = 'CancelFeedSubmissions'

		if submissions is not None:
			args.update(submission_args(submissions, name='submissions'))

		if feed_types is not None:
			args.update(feed_type_args(feed_types, name='feed_types'))

		if from_date is not None:
			args['SubmittedFromDate'] = datetime_to_iso8601(from_date, name='from_date')

		if to_date is not None:
			args['SubmittedToDate'] = datetime_to_iso8601(to_date, name='to_date')

		# Send request.
		return self.send_request(args, debug=debug)

	def count_submissions(self, feed_types=None, statuses=None, from_date=None, to_date=None, debug=None):
		"""
		Requests a count of all Feed Submissions that match the specified
		criteria.

		*feed_types* (**sequence**) contains each Feed Type (``str``) to
		filter the list of submissions to count. This can contain any keys
		or values from ``FEED_TYPES``. Default is ``None`` for all Feed
		Types.

		*statuses* (**sequence**) contains each Processing Status
		(``str``) to filter the list of submissions to count. This can
		contain keys or values from ``PROCESSING_STATUSES``. Default is

		*from_date* (``datetime.datetime`` or ``float``) is the earliest
		date to filter the list of submissions to count. Default is
		``None`` for 90 days ago.

		*to_date* (``datetime.datetime`` or ``float``) is the latest date to
		filter the list of submissions to cancel. count is ``None`` for
		now.

		Returns the response XML (``str``).
		"""
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetFeedSubmissionCount'

		if feed_types is not None:
			args.update(feed_type_args(feed_types, name='feed_types'))

		if statuses is not None:
			args.update(status_args(statuses, name='statuses'))

		if from_date is not None:
			args['SubmittedFromDate'] = datetime_to_iso8601(from_date, name='from_date')

		if to_date is not None:
			args['SubmittedToDate'] = datetime_to_iso8601(to_date, name='to_date')

		# Send request.
		return self.send_request(args, debug=debug)

	def get_report(self, submission_id, debug=None):
		"""
		Requests the Feed Processing Report.

		*submission_id* (``str``) is the ID of the Feed Submission.

		Returns the response XML (``str``).
		"""
		if not isinstance(submission_id, basestring):
			raise TypeError("submission_id:{!r} is not a string.".format(submission_id))
		elif not submission_id:
			raise ValueError("submission_id:{!r} cannot be empty.".format(submission_id))
		submission_id = submission_id.encode('ASCII')

		# Buils args.
		args = self.new_args()
		args['Action'] = 'GetFeedSubmissionResult'
		args['FeedSubmissionId'] = submission_id

		# Send request.
		return self.send_request(args, debug=debug)

	def list_submissions(self, submissions=None, count=None, feed_types=None, statuses=None, from_date=None, to_date=None, debug=None):
		"""
		Requests for the list of Feed Submissions that match the specified
		criteria.

		To list only specific Feed Submissions, set *submissions*.

		*submissions* (**sequence**) contains the ID (``str``) of each Feed
		Submission to list.

		To list Feed Submissions based upon a query, use the following:

		*count* (``int``) is the maximum number of Feed Submissions to
		list. This cannot exceed 100. Default is ``None`` for 10.

		*feed_types* (**sequence**) contains each Feed Type (``str``) to
		filter the list of submissions to list. This can contain any of the
		keys or values in ``FEED_TYPES``. Default is ``None`` for all Feed
		Types.

		*statuses* (**sequence**) contains each Processing Status
		(``str``) to filter the list of submissions to count. This can
		contain any of the keys or values from ``PROCESSING_STATUSES``.
		Default is ``None`` for all Processing Statuses.

		*from_date* (``datetime.datetime`` or ``float``) is the earliest
		date to filter the list of submissions to count. Default is
		``None`` for 180 days ago.

		*to_date* (``datetime.datetime`` or ``float``) is the latest date to
		filter the list of submissions to cancel. count is ``None`` for
		now.

		Returns the response XML (``str``).
		"""
		if submissions is not None and (count is not None or feed_types is not None or statuses is not None or from_date is not None or to_date is not None):
			raise ValueError("Only submissions:{subs!r}, or a query (count:{count!r}, feed_types:{feed_types!r}, statuses:{statuses!r}, from_date:{from_date!r}, and to_date:{to_date!r}) can be set.".format(
				subs=submissions,
				count=count,
				feed_types=feed_types,
				statuses=statuses,
				from_date=from_date,
				to_date=to_date
			))

		# Build args.
		args = self.new_args()
		args['Action'] = 'GetFeedSubmissionList'

		if submissions is not None:
			args.update(submission_args(submissions, name='submissions'))

		if count is not None:
			if not isinstance(count, (int, long)):
				raise TypeError("count:{!r} is not an integer.".format(count))
			elif count < 1 or 100 < count :
				raise ValueError("count:{!r} is not between 1 and 100 inclusive.".format(count))
			args['MaxCount'] = str(count)

		if feed_types is not None:
			args.update(feed_type_args(feed_types, name='feed_types'))

		if statuses is not None:
			args.update(status_args(statuses, name='statuses'))

		if from_date is not None:
			args['SubmittedFromDate'] = datetime_to_iso8601(from_date, name='from_date')

		if to_date is not None:
			args['SubmittedToDate'] = datetime_to_iso8601(to_date, name='to_date')

		# Send request.
		return self.send_request(args, debug=debug)

	def list_submissions_next(self, next_token, debug=None):
		"""
		Requests the next batch of Feed Submissions being listed.

		*next_token* (``str``) is the token used to fetch the next batch of
		results.

		Returns the response XML (``str``).
		"""
		if not isinstance(next_token, basestring):
			raise TypeError("next_token:{!r} is not a string.".format(next_token))
		elif not next_token:
			raise ValueError("next_token:{!r} cannot be empty.".format(next_token))
		next_token = next_token.encode('ASCII')

		# Build args.
		args = self.new_args()
		args['Action'] = 'GetFeedSubmissionListByNextToken'
		args['NextToken'] = next_token

		# Send request.
		return self.send_request(args, debug=debug)

	def submit_feed(self, feed_type, data, content_type, marketplaces=None, debug=None):
		"""
		Submits the specified feed.

		*feed_type* (``str``) is the type of feed being submitted. This can
		be any of the keys or values from ``FEED_TYPES``.

		*data* (``str`` or ``file``) is the feed data. This can be either
		the raw bytes (``str``) or a ``file`` object supporting ``read()``.

		*content_type* (``str``) is the content type of *data*.

		*marketplaces* (**sequence**) optionally contains the ID (``str``)
		of each Amazon Marketplace to apply the feed to. Default is ``None``
		for all Amazon Marketplaces.

		Returns the response XML (``str``).
		"""
		if not isinstance(feed_type, str):
			raise TypeError("feed_type:{!r} is not a str.".format(feed_type))
		if data is None:
			raise TypeError("data:{!r} is not a str or file.".format(data))

		args = self.new_args()
		args['Action'] = 'SubmitFeed'
		args['FeedType'] = FEED_TYPES.get(feed_type, feed_type)

		if marketplaces is not None:
			args.update(marketplace_args(marketplaces, name='marketplaces'))

		return self.send_request(args, body=data, content_type=content_type, debug=debug)


def feed_type_args(feed_types, name=None):
	"""
	Converts the specified Feed Types into their resepctive URL query
	arguments.

	*feed_types* (**sequence**) contains each Feed Type (``str``). This
	can contain any of the keys or values from ``FEED_TYPES``.

	*name* (``str``) is the name to use when an error occurs.

	Returns a ``list`` containing each *key*-*feed_type* ``tuple``.

		- *key* (``str``) is the query argument key for *feed_type*.

		- *feed_type* (``str``) is the Feed Type ID.
	"""
	if not name:
		name = 'feed_types'

	if not is_sequence(feed_types):
		raise TypeError("{}:{!r} is not a sequence.".format(name, feed_types))

	args = []
	for i, feed_type in enumerate(feed_types):
		feed_type = FEED_TYPES.get(feed_type, feed_type)
		if not isinstance(feed_type, str):
			raise TypeError("{}[{}]:{!r} is not a str.".format(name, i, feed_type))
		elif not feed_type:
			raise ValueError("{}[{}]:{!r} cannot be empty.".format(name, i, feed_type))
		feed_type = encode_string(feed_type, 'ASCII', name="{}[{}]".format(name, i))

		args.append(('FeedTypeList.Type.{}'.format(i + 1), feed_type))

	return args

def status_args(statuses, name=None):
	"""
	Converts the specified Feed Processing Statuses into their respective
	URL query arguments.

	*statuses* (**sequence**) contains each Feed Processing Status
	(``str``). This can contain any of the keys or value from ``PROCESSING_STATUSES``.

	*name* (``str``) is the name to use when an error occurs.

	Returns a ``list`` containing each *key*-*status* ``tuple``.

		- *key* (``str``) is the query argument key for *status*.

		- *status* (``str``) is the Feed Processing Status.
	"""
	if not name:
		name = 'statuses'

	if not is_sequence(statuses):
		raise TypeError("{}:{!r} is not a sequence.".format(name, statuses))

	args = []
	for i, status in enumerate(statuses):
		status = PROCESSING_STATUSES.get(status, status)
		if not isinstance(status, str):
			raise TypeError("{}[{}]:{!r} is not a str.".format(name, i, status))
		elif not status:
			raise ValueError("{}[{}]:{!r} cannot be empty.".format(name, i, status))
		status = encode_string(status, 'ASCII', name="{}[{}]".format(name, i))

		args.append(('FeedProcessingStatusList.Status.{}'.format(i + 1), status))

	return args

def submission_args(submissions, name=None):
	"""
	Converts the specified Feed Submission IDs into their resepctive URL
	query arguments.

	*submissions* (**sequence**) contains each Feed Submission ID
	(``str``).

	*name* (``str``) is the name to use when an error occurs.

	Returns a ``list`` containing each *key*-*submission_id* ``tuple``.

		- *key* (``str``) is the query argument key for *submission_id*.

		- *submission_id* (``str``) is the Feed Submission ID.
	"""
	if not name:
		name = 'submissions'

	if not is_sequence(submissions):
		raise TypeError("{}:{!r} is not a sequence.".format(name, submissions))

	args = []
	for i, sub_id in enumerate(submissions):
		if not isinstance(sub_id, basestring):
			raise TypeError("{}[{}]:{!r} is not a string.".format(name, i, sub_id))
		elif not sub_id:
			raise ValueError("{}[{}]:{!r} cannot be empty.".format(name, i, sub_id))
		sub_id = encode_string(sub_id, 'ASCII', name="{}[{}]".format(name, i))

		args.append(('FeedSubmissionIdList.Id.{}'.format(i + 1), sub_id))

	return args
