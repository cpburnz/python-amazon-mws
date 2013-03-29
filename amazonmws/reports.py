# coding: utf-8
"""
This module provides an implementation of the Amazon MWS Reports API.
"""

__created__ = "2012-12-31"
__modified__ = "2013-03-25"

import datetime

import amazonmws.mws
from amazonmws.util import datetime_to_iso8601, encode_string, is_sequence, marketplace_args

#: Report types.
REPORT_TYPES = {
	'listing_cancelled': '_GET_MERCHANT_CANCELLED_LISTINGS_DATA_',
	'listing_compat': '_GET_MERCHANT_LISTINGS_DATA_BACK_COMPAT_',
	'listing_data': '_GET_MERCHANT_LISTINGS_DATA_',
	'listing_defect': '_GET_MERCHANT_LISTINGS_DEFECT_DATA_',
	'listing_lite': '_GET_MERCHANT_LISTINGS_DATA_LITE_',
	'listing_liter': '_GET_MERCHANT_LISTINGS_DATA_LITER_',
	'listing_open': '_GET_FLAT_FILE_OPEN_LISTINGS_DATA_',
	'order_actionable': '_GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_',
	'order_data': '_GET_FLAT_FILE_ORDERS_DATA_',
	'order_reports': '_GET_FLAT_FILE_ORDER_REPORT_DATA_',
	'order_reports_converged': '_GET_CONVERGED_FLAT_FILE_ORDER_REPORT_DATA_',
	'settlement_alt': '_GET_ALT_FLAT_FILE_PAYMENT_SETTLEMENT_DATA_',
	'settlement_csv': '_GET_FLAT_FILE_PAYMENT_SETTLEMENT_DATA_',
	'settlement_xml': '_GET_PAYMENT_SETTLEMENT_DATA_',
}

#: Report schedules.
REPORT_SCHEDULES = {
	'15_min': '_15_MINUTES_',
	'20_min': '_30_MINUTES_',
	'1_hr': '_1_HOUR_',
	'2_hr': '_2_HOURS_',
	'4_hr': '_4_HOURS_',
	'8_hr': '_8_HOURS_',
	'12_hr': '_12_HOURS_',
	'72_hr': '_72_HOURS_',
	'1_day': '_1_DAYS_',
	'2_day': '_2_DAYS_',
	'3_day': '_72_HOURS_',
	'7_day': '_7_DAYS_',
	'14_day': '_14_DAYS_',
	'15_day': '_15_DAYS_',
	'30_day': '_30_DAYS_',
	'never': '_NEVER_',
}

#: Report processing statuses.
REPORT_STATUSES = {
	'cancelled': '_CANCELLED_',
	'done': '_DONE_',
	'done_no_data': '_DONE_NO_DATA_',
	'in_progress': '_IN_PROGRESS_',
	'submitted': '_SUBMITTED_',
}


class MWSReports(amazonmws.mws.MWS):
	"""
	The ``MWSReports`` class is used to send requests to the Amazon MWS
	Reports API. The primary purpose of this class is to allow sellers to
	request various reports.
	"""
	
	client_api_version = __modified__
	"""
	*client_api_version* (``str``) is the version of this client API.
	"""
	
	reports_api_version = '2009-01-01'
	"""
	*products_api_version* (``str``) is the version of the MWS Products
	API implemented.
	"""
	
	path = "/"
	"""
	*path* (``str``) is path all Sellers API requests are sent to.
	"""
	
	def cancel_report_requests(self, requests=None, report_types=None, statuses=None, from_date=None, to_date=None, marketplaces=None, debug=None):
		"""
		Cancels all Report Requests that match the query.
		
		.. NOTE:: Report Requests that have already begun processing cannot
		   be cancelled.
		
		To cancel Report Requests based upon ID use *requests*.
		
		*requests* (**sequence**) is used to filter on Report Request ID
		(``str``). If not ``None``, no other query arguments will be used
		and only those Report Requests with matching IDs will be returned.
		Default is ``None`` to not use Report Request IDs.
		
		To cancel Report Requests based upon a query use any combination of
		the following: *report_types*, *statuses*, *from_date*, *to_date*,
		and *marketplaces*.
		
		*report_types* (**sequence**) is used to filter on Report Type
		(``str``). This can contain any keys or values from
		``REPORT_TYPES``. Default is ``None`` to not filter on Report Type.
		
		*statuses* (**sequence**) is used to filter on Report Processing
		Status (``str``). This can contain any keys or values from
		``REPORT_STATUSES``. Default is ``None`` to not filter on Report
		Processing Status.
		
		*from_date* (``datetime`` or ``float``) is the start of the date
		range to use for selecting Report Requests. Default is ``None`` for
		90 days ago.
		
		*to_date* (``datetime`` or ``float``) is the end of the date range
		to use for selecting Report Requests. Default is ``None`` for now.
		
		*marketplaces* (**sequence**) is the list of Amazon Marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		
		Returns the raw XML response (``str``).
		"""
		if from_date is not None:
			from_date = datetime_to_iso8601(from_date, name='from_date')
		
		if to_date is not None:
			to_date = datetime_to_iso8601(to_date, name='to_date')
		
		# Build args.
		args = self.new_args()
		args['Action'] = 'CancelReportRequests'
		
		if requests:
			args.update(request_args(requests, name='requests'))
				
		else:
			if report_types is not None:
				args.update(report_type_args(report_types, name='report_types'))
					
			if statuses is not None:
				args.update(status_args(statuses, name='statuses'))
					
			if from_date:
				args['RequestedFromDate'] = from_date
				
			if to_date:
				args['RequestedToDate'] = to_date
				
			if marketplaces is not None:
				args.update(marketplace_args(marketplaces, name='marketplaces'))
				
		# Send request.
		return self.send_request(args, debug=debug)
	
	def get_report(self, report_id, marketplaces=None, debug=None):
		"""
		Gets the contents of the Report.
		
		*report_id* (``int``) is the Report ID.
		
		*marketplaces* (**sequence**) is the list of marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		
		Returns the contents of the Report.
		"""
		if not isinstance(report_id, (int, long)):
			raise TypeError("report_id:{!r} is not an integer.".format(report_id))
		elif report_id < 0:
			raise ValueError("report_id:{!r} cannot be less than 0.".format(report_id))
			
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetReport'
		args['ReportId'] = report_id
			
		if marketplaces is not None:
			args.update(marketplace_args(marketplaces, name='marketplaces'))
			
		# Send request.
		return self.send_request(args, debug=debug)
	
	def get_report_count(self, report_types=None, acknowledged=None, from_date=None, to_date=None, marketplaces=None, debug=None):
		"""
		Gets the total number of Reports that match the query.
		
		*report_types* (**sequence**) is used to filter on Report Type
		(``str``). This can contain any keys or values from
		``REPORT_TYPES``. Default is ``None`` to not filter on Report Type.
		
		*acknowledged* (``bool``) is used to filter on whether Order Reports
		have been acknowledged (``True``), or not (``False``). Default is
		``None`` to not filter on Acknowledged state. 
		
		.. NOTE:: Setting *acknowledged* to ``True`` will result in only
		   Order Reports (not Listing Reports) being returned.
		
		*from_date* (``datetime`` or ``float``) is the start of the date
		range to use for selecting Report Requests. Default is ``None`` for
		90 days ago.
		
		*to_date* (``datetime`` or ``float``) is the end of the date range
		to use for selecting Report Requests. Default is ``None`` for now.
		
		*marketplaces* (**sequence**) is the list of Amazon Marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		
		Returns the raw XML response (``str``).
		"""
		if acknowledged is not None:
			acknowledged = bool(acknowledged)
			
		if from_date is not None:
			from_date = datetime_to_iso8601(from_date, name='from_date')
			
		if to_date is not None:
			to_date = datetime_to_iso8601(to_date, name='to_date')
			
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetReportCount'
		
		if report_types is not None:
			args.update(report_type_args(report_types, name='report_types'))
				
		if acknowledged is not None:
			args['Acknowledged'] = 'true' if acknowledged else 'false'
			
		if from_date:
			args['RequestedFromDate'] = from_date
			
		if to_date:
			args['RequestedToDate'] = to_date
			
		if marketplaces is not None:
			args.update(marketplace_args(marketplaces, name='marketplaces'))
			
		# Send request.
		return self.send_request(args, debug=debug)
		
	def get_report_list(self, requests=None, max_count=None, report_types=None, acknowledged=None, from_date=None, to_date=None, marketplaces=None, debug=None):
		"""
		Lists the Reports that match the query.
		
		To list Reports based upon Request ID use *requests*.
		
		*requests* (**sequence**) is used to filter on Report Request ID
		(``str``). If not ``None``, no other query arguments will be used
		and only those Report Requests with matching IDs will be returned.
		Default is ``None`` to not use Report Request IDs.
		
		To list Reports based upon a query use any combination of the
		following: *max_count*, *report_types*, *acknowledged*, *from_date*,
		*to_date*, and *marketplaces*.
		
		*max_count* (``int``) is the maximum number of Reports to return per
		response. This must between 1 and 100 inclusive. Default is 10.
		
		*report_types* (**sequence**) is used to filter on Report Type
		(``str``). This can contain any keys or values from
		``REPORT_TYPES``. Default is ``None`` to not filter on Report Type.
		
		*acknowledged* (``bool``) is used to filter on whether Order Reports
		have been acknowledged (``True``), or not (``False``). Default is
		``None`` to not filter on Acknowledged state.
		
		.. NOTE:: Setting *acknowledged* to ``True`` will result in only
		   Order Reports (not Listing Reports) being returned.
		
		*from_date* (``datetime`` or ``float``) is the start of the date
		range to use for selecting Report Requests. Default is ``None`` for
		90 days ago.
		
		*to_date* (``datetime`` or ``float``) is the end of the date range
		to use for selecting Report Requests. Default is ``None`` for now.
		
		*marketplaces* (**sequence**) is the list of Amazon Marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		
		Returns the raw XML response (``str``).
		"""
		if max_count is not None:
			if not isinstance(max_count, (int, long)):
				raise TypeError("max_count:{!r} is not an int.".format(max_count))
			elif max_count < 1 or 100 < max_count:
				raise ValueError("max_count:{!r} is not between 1 and 100 inclusive.".format(max_count))
				
		if acknowledged is not None:
			acknowledged = bool(acknowledged)
			
		if from_date is not None:
			from_date = datetime_to_iso8601(from_date, name='from_date')
			
		if to_date is not None:
			to_date = datetime_to_iso8601(to_date, name='to_date')
			
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetReportList'
		
		if requests:
			args.update(request_args(requests, name='requests'))
				
		else:
			if max_count:
				args['MaxCount'] = max_count
		
			if report_types is not None:
				args.update(report_type_args(report_types, name='report_types'))
					
			if acknowledged is not None:
				args['Acknowledged'] = 'true' if acknowledged else 'false'
				
			if from_date:
				args['RequestedFromDate'] = from_date
				
			if to_date:
				args['RequestedToDate'] = to_date
				
			if marketplaces is not None:
				args.update(marketplace_args(marketplaces, name='marketplaces'))
		
		# Send request.
		return self.send_request(args, debug=debug)
	
	def get_report_list_next(self, next_token, debug=None):
		"""
		Requests the next batch of Reports that match the original Get
		Report List query.
		
		*next_token* (``str``) is the token returned from the last request.
		
		Returns the raw XML response (``str``).
		"""
		if not isinstance(next_token, basestring):
			raise TypeError("next_token:{!r} is not a string.".format(next_token))
		elif not next_token:
			raise ValueError("next_token:{!r} cannot be empty.".format(next_token))
		next_token = next_token.encode('ASCII')
			
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetReportListByNextToken'
		args['NextToken'] = next_token
		
		# Send request.
		return self.send_request(args, debug=debug)
		
	def get_report_request_count(self, report_types=None, statuses=None, from_date=None, to_date=None, marketplaces=None, debug=None):
		"""
		Gets the total number of Report Requests that match the query.
		
		*report_types* (**sequence**) is used to filter on Report Type
		(``str``). This can contain any keys or values from
		``REPORT_TYPES``. Default is ``None`` to not filter on Report Type.
		
		*statuses* (**sequence**) is used to filter on Report Processing
		Status (``str``). This can contain any keys or values from
		``REPORT_STATUSES``. Default is ``None`` to not filter on Report
		Processing Status.
		
		*from_date* (``datetime`` or ``float``) is the start of the date
		range to use for selecting Report Requests. Default is ``None`` for
		90 days ago.
		
		*to_date* (``datetime`` or ``float``) is the end of the date range
		to use for selecting Report Requests. Default is ``None`` for now.
		
		*marketplaces* (**sequence**) is the list of Amazon Marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		
		Returns the raw XML response (``str``).
		"""
		if from_date is not None:
			from_date = datetime_to_iso8601(from_date, name='from_date')
			
		if to_date is not None:
			to_date = datetime_to_iso8601(to_date, name='to_date')
			
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetReportRequestCount'
		
		if report_types is not None:
			args.update(report_type_args(report_types, name='report_types'))
			
		if statuses is not None:
			args.update(status_args(statuses, name='statuses'))
				
		if from_date:
			args['RequestedFromDate'] = from_date
			
		if to_date:
			args['RequestedToDate'] = to_date
			
		if marketplaces is not None:
			args.update(marketplace_args(marketplaces, name='marketplaces'))
			
		# Send request.
		return self.send_request(args, debug=debug)
			
	def get_report_request_list(self, requests=None, max_count=None, report_types=None, statuses=None, from_date=None, to_date=None, marketplaces=None, debug=None):
		"""
		Requests for the list of Report Requests that match the query.
		
		To list Report Requests based upon ID use *requests*.
		
		*requests* (**sequence**) is used to filter on Report Request ID
		(``str``). If not ``None``, no other query arguments will be used
		and only those Report Requests with matching IDs will be returned.
		Default is ``None`` to not use Report Request IDs.
		
		To list Report Requests based upon a query use any combination of
		the following: *max_count*, *report_types*, *statuses*, *from_date*,
		*to_date*, and *marketplaces*.
		
		*max_count* (``int``) is the maximum number of Report Requests to
		return per response. This must between 1 and 100 inclusive. Default
		is 10.
		
		*report_types* (**sequence**) is used to filter on Report Type
		(``str``). This can contain any keys or values from
		``REPORT_TYPES``. Default is ``None`` to not filter on Report Type.
		
		*statuses* (**sequence**) is used to filter on Report Processing
		Status (``str``). This can contain any keys or values from
		``REPORT_STATUSES``. Default is ``None`` to not filter on Report
		Processing Status.
		
		*from_date* (``datetime`` or ``float``) is the start of the date
		range to use for selecting Report Requests. Default is ``None`` for
		90 days ago.
		
		*to_date* (``datetime`` or ``float``) is the end of the date range
		to use for selecting Report Requests. Default is ``None`` for now.
		
		*marketplaces* (**sequence**) is the list of Amazon Marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		
		Returns the raw XML response (``str``).
		"""
		if max_count is not None:
			if not isinstance(max_count, (int, long)):
				raise TypeError("max_count:{!r} is not an int.".format(max_count))
			elif max_count < 1 or 100 < max_count:
				raise ValueError("max_count:{!r} is not between 1 and 100 inclusive.".format(max_count))
				
		if from_date is not None:
			from_date = datetime_to_iso8601(from_date, name='from_date')
		
		if to_date is not None:
			to_date = datetime_to_iso8601(to_date, name='to_date')
			
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetReportRequestList'
		
		if requests:
			args.update(request_args(requests, name='requests'))
				
		else:
			if max_count:
				args['MaxCount'] = max_count
			
			if report_types is not None:
				args.update(report_type_args(report_types, name='report_types'))
					
			if statuses is not None:
				args.update(status_args(statuses, name='statuses'))
					
			if from_date:
				args['RequestedFromDate'] = from_date
				
			if to_date:
				args['RequestedToDate'] = to_date
				
			if marketplaces is not None:
				args.update(marketplace_args(marketplaces, name='marketplaces'))
		
		# Send request.
		return self.send_request(args, debug=debug)
		
	def get_report_request_list_next(self, next_token, debug=None):
		"""
		Requests the next batch of Report Requests that match the original
		Get Report Request List query.
		
		*next_token* (``str``) is the token returned from the last request.
		
		Returns the raw XML response (``str``).
		"""
		if not isinstance(next_token, basestring):
			raise TypeError("next_token:{!r} is not a str.".format(next_token))
		elif not next_token:
			raise ValueError("next_token:{!r} cannot be empty.".format(next_token))
		next_token = next_token.encode('ASCII')
			
		# Build args.
		args = self.new_args()
		args['Action'] = 'GetReportRequestListByNextToken'
		args['NextToken'] = next_token
			
		# Send request.
		return self.send_request(args, debug=debug)
	
	def new_args(self):
		"""
		Returns a new set of default arguments (``dict``).
		
		*marketplaces* (**sequence**) is the list of marketplace IDs
		(``str``). Default is ``None``.
		"""
		return {
			'AWSAccessKeyId': self.access_key,
			'SellerId': self.merchant_id,
			'Timestamp': datetime_to_iso8601(datetime.datetime.utcnow()),
			'Version': self.reports_api_version
		}
	
	def request_report(self, report_type, start_date=None, end_date=None, show_sales_channel=None, marketplaces=None, debug=None):
		"""
		Requests that the specified Report be created.
		
		*report_type* (``str``) is the report type.
		
		*start_date* (``datetime`` or ``float``) is the start of the date
		range used for selecting the data to report. Default is ``None`` for
		now.
		
		*end_date* (``datetime`` or ``float``) is the end of the date range
		used for selecting the data to report. Default is ``None`` for now.
		
		*show_sales_channel* (``bool``) indicates that an additional column
		for several Order Reports should be shown (``True``), or not
		(``False``). Default is ``None`` to not show the additional column.
		
		*marketplaces* (**sequence**) is the list of Amazon Marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		
		Returns the Report Request ID (``str``) if the response is to be
		parsed; otherwise, the raw XML response (``str``)
		"""
		report_type = REPORT_TYPES.get(report_type, report_type)
		if not isinstance(report_type, basestring):
			raise TypeError("report_type:{!r} is not a string.".format(report_type))
		elif not report_type:
			raise ValueError("report_type:{!r} cannot be empty.".format(report_type))
		report_type = report_type.encode('ASCII')
		
		if start_date is not None:
			start_date = datetime_to_iso8601(start_date, name='start_date')
			
		if end_date is not None:
			end_date = datetime_to_iso8601(end_date, name='end_date')
			
		if show_sales_channel is not None:
			show_sales_channel = bool(show_sales_channel)
		
		# Build request.
		args = self.new_args()
		args['Action'] = 'RequestReport'
		args['ReportType'] = report_type
		
		if start_date:
			args['StartDate'] = start_date
			
		if end_date:
			args['EndDate'] = end_date
			
		if show_sales_channel is not None:
			args['ReportOptions=ShowSalesChannel'] = 'true' if show_sales_channel else 'false'
	
		if marketplaces is not None:
			args.update(marketplace_args(marketplaces, name='marketplaces'))
			
		# Send request.
		return self.send_request(args, debug=debug)
	
	def update_report_acknowledgements(self, reports, marketplaces=None, debug=None):
		"""
		Updates the acknowledged status of the specified Reports.
		
		*reports* (**sequence**) is the list of Report IDs (``int``) to
		update. The maximum number of Reports that can be specified is 100.
		
		*marketplaces* (**sequence**) is the list of Amazon Marketplace IDs
		(``str``). Default is ``None`` for all marketplaces.
		"""
		if not is_sequence(reports):
			raise TypeError("reports:{!r} is not a sequence.".format(reports))
		elif len(reports) < 0 or 100 < len(reports):
			raise ValueError("reports len:{!r} must be between 1 and 100 inclusive.".format(len(reports)))
		
		# Build args.
		args = self.new_args()
		args['Action'] = 'UpdateReportAcknowledgements'
		args['Acknowledged'] = 'true'
			
		for i, report_id in enumerate(reports, 0):
			if not isinstance(report_id, basestring):
				raise TypeError("reports[{}]:{!r} is not a string.".format(i, report_id))
			elif not report_id:
				raise ValueError("reports[{}]:{!r} cannot be empty.".format(i, report_id))
			report_id = encode_string(report_id, 'ASCII', name="reports[{}]".format(i))
			
			args['ReportIdList.Id.{}'.format(report_id)] = report_id
			
		if marketplaces is not None:
			args.update(marketplace_args(marketplaces, name='marketplaces'))
		
		# Send Request.
		return self.send_request(args, debug=debug)
		
	def manage_report_schedule(self):
		# TODO
		raise NotImplementedError()
		
	def get_report_schedule_count(self):
		# TODO
		raise NotImplementedError()
		
	def get_report_schedule_list(self):
		# TODO
		raise NotImplementedError()
		
	def get_report_schedule_list_next(self):
		# TODO
		raise NotImplementedError()
		
		
def report_type_args(report_types, name=None):
	"""
	Converts the specified Report Types into their respective URL query
	arguments.
	
	*report_types* (**sequence**) contains each Report Type (``str``).
	This can contain any keys or values from ``REPORT_TYPES``.
	
	*name* (``str``) is the name to use when an error occurs.
	
	Returns a ``list`` containing each *key*-*report_type* ``tuple``.
	
		- *key* (``str``) is the query argument key for *report_type*.
		
		- *report_type* (``str``) is the Report Type.
	"""
	if not name:
		name = 'report_types'

	if not is_sequence(report_types):
		raise TypeError("{}:{!r} is not a sequence.".format(name, report_types))
		
	args = []
	for i, report_type in enumerate(report_types, 0):
		report_type = REPORT_TYPES.get(report_type, report_type)
		if not isinstance(report_type, basestring):
			raise TypeError("{}[{}]:{!r} is not a string.".format(name, i, report_type))
		elif not report_type:
			raise ValueError("{}[{}]:{!r} cannot be empty.".format(name, i, report_type))
		report_type = encode_string(report_type, 'ASCII', name="{}[{}]".format(name, i))
		
		args.append(('ReportTypeList.Type.{}'.format(i + 1), report_type))

	return args
	
def request_args(requests, name=None):
	"""
	Converts the specified Report Request IDs into their respective URL
	query arguments.
	
	*requests* (**sequence**) contains each Report Request ID (``str``).
		
	*name* (``str``) is the name to use when an error occurs.
	
	Returns a ``list`` containing each *key*-*request_id* ``tuple``.
	
		- *key* (``str``) is the query argument key for *request_id*.
		
		- *request_id* (``str``) is the Report Request ID.
	"""
	if not name:
		name = 'requests'

	if not is_sequence(requests):
		raise TypeError("{}:{!r} is not a sequence.".format(name, requests))
		
	args = []
	for i, request_id in enumerate(requests, 0):
		if not isinstance(request_id, basestring):
			raise TypeError("{}[{}]:{!r} is not a string.".format(name, i, request_id))
		elif not request_id:
			raise ValueError("{}[{}]:{!r} cannot be empty.".format(name, i, request_id))
		request_id = encode_string(request_id, 'ASCII', name="{}[{}]".format(name, i))
		
		args.append(('ReportRequestIdList.Id.{}'.format(i + 1), request_id))

	return args
	
def status_args(statuses, name=None):
	"""
	Converts the specified Report Processing Status into their respective
	URL query arguments.
	
	*statuses* (**sequence**) contains each Report Processing Status
	(``str``). This contain any keys or values from ``REPORT_STATUSES``.
		
	*name* (``str``) is the name to use when an error occurs.
	
	Returns a ``list`` containing each *key*-*status* ``tuple``.
	
		- *key* (``str``) is the query argument key for *status*.
		
		- *request_id* (``str``) is the Report Processing Status.
	"""
	if not name:
		name = 'statuses'

	if not is_sequence(statuses):
		raise TypeError("{}:{!r} is not a statuses.".format(name, statuses))
		
	args = []
	for i, status in enumerate(statuses, 0):
		if not isinstance(status, basestring):
			raise TypeError("{}[{}]:{!r} is not a string.".format(name, i, status))
		elif not status:
			raise ValueError("{}[{}]:{!r} cannot be empty.".format(name, i, status))
		status = encode_string(status, 'ASCII', name="{}[{}]".format(name, i))
		
		args.append(('ReportProcessingStatusList.Status.{}'.format(i + 1), status))

	return args
