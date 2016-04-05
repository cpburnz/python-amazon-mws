# coding: utf-8
"""
This module contains utility methods that are not necessarily specific
to Amazon MWS, but are used throughout the implementation of its APIs.
"""

__author__ = "Caleb P. Burns"
__created__ = "2012-11-26"
__modified__ = "2016-03-29"
__modified_by___ = "Joshua D. Burns"

import six # Python2/Python3 compatibility library.
import collections
import datetime

def datetime_to_iso8601(dt, name=None):
	"""
	Formats a datetime as an ISO 8601 string.

	*dt* is the datetime. If this is a ``float`` (or ``int`` or ``long``),
	it will be considered to be the seconds passed since the UNIX epoch
	relative to UTC. If this is a **naive** ``datetime``, it will also be
	considered relative to UTC. If this is a ``date``, it will be
	converted a ``datetime`` at midnight relative to UTC.

	*name* (``str``) is the name to use when an error occurs.

	Returns the formatted datetime (``str``).
	"""
	if not isinstance(dt, datetime.datetime):
		if isinstance(dt, (float,)) or isinstance(dt, six.integer_types):
			dt = datetime.datetime.utcfromtimestamp(dt)
		elif isinstance(dt, datetime.date):
			dt = datetime.datetime.combine(dt, datetime.time(0))
		else:
			raise TypeError("{}:{!r} is not a datetime or float.".format(name or 'dt', dt))
	datestr = dt.isoformat()
	if dt.utcoffset() is None:
		datestr += '+00:00'
	return datestr

def encode_string(value, encoding, name=None):
	"""
	Encodes the specified string.

	*value* (**string**) is the string to encode.

	*encoding* (``str``) is the encoding to use.

	*name* (``str``) is the name to use when an error occurs.

	Returns the encoded string (``str``).
	"""
	try:
		return value.encode(encoding)
	except UnicodeDecodeError as e:
		if name:
			raise UnicodeDecodeError(e.encoding, e.object, e.start, e.end, e.reason + " for {}".format(name))
		raise

def is_sequence(obj):
	"""
	Determines whether the specified object is a sequence.

	.. NOTE:: This excludes strings.

	*obj* (``object``) is the object to check.

	Returns whether the specified object is a sequence (``bool``).
	"""
	return isinstance(obj, collections.Sequence) and not isinstance(obj, six.string_types)

def marketplace_args(marketplaces, name=None):
	"""
	Converts the specified Amazon Marketplace IDs into their respective
	URL query arguments.

	*marketplaces* (``sequence``) contains each Amazon Marketplace ID
	(``str``).

	*name* (``str``) is the name to use when an error occurs.

	Returns a ``list`` containing each *key*-*marketplace_id* ``tuple``.

		- *key* (``str``) is the query argument key for *marketplace_id*.

		- *marketplace_id* (``str``) is the Amazon Marketplace ID.
	"""
	if not name:
		name = 'marketplaces'

	if not is_sequence(marketplaces):
		raise TypeError("{}:{!r} is not a sequence.".format(name, marketplaces))

	args = []
	for i, marketplace_id in enumerate(marketplaces, 0):
		if not isinstance(marketplace_id, six.string_types):
			raise TypeError("{}[{}]:{!r} is not a string.".format(name, i, marketplace_id))
		elif not marketplace_id:
			raise ValueError("{}[{}]:{!r} cannot be empty.".format(name, i, marketplace_id))
		#marketplace_id = encode_string(marketplace_id, 'ASCII', name="{}[{}]".format(name, i)) # TODO: Why were we encoding? This was causing issues in python 3.

		args.append(('MarketplaceIdList.Id.{}'.format(i + 1), marketplace_id))

	return args

def validate_dict(value, name=None, keys=None):
	"""
	Validates the specified dictionary.

	*value* (``dict``) is the dictionary to validate.

	*name* (``str``) optionally is the name to use when an error occurs.

	*keys* (**sequence**) optionally contains each key (``object``) that
	must be in *value*.

	Raises an ``Exception`` if *value* is not valid.
	"""
	if not name:
		name = 'value'

	if not isinstance(value, dict):
		raise TypeError("{}:{!r} is not a dict.".format(name, value))

	if keys is not None:
		for key in keys:
			if key not in value:
				raise KeyError("{}[{!r}] is not set.".format(name, key))

def validate_float(value, name=None, range_=None):
	"""
	Validates the specified float.

	*value* (``float``) is the float to validate.

	*name* (``str``) optionally is the name to use when an error occurs.

	*range_* (``tuple``) optionally contains: the minumum (``float``) and
	maximum (``float``) values of *value*. The minimum and maximum values
	can be ``None`` for no restriction. Default is ``None`` for
	``(None, None)``.

	Raises an ``Exception`` if *value* is not valid.
	"""
	if not name:
		name = 'value'
	if range_ is not None:
		min_, max_ = range_
	else:
		min_ = None
		max_ = None

	if not isinstance(value, (float,)) or isinstance(value, six.integer_types):
		raise TypeError("{}:{!r} is not a float.".format(name, value))

	if min_ is not None and value < min_:
		raise ValueError("{}:{!r} cannot be less than {}.".format(name, value, min_))
	elif max_ is not None and value > max_:
		raise ValueError("{}:{!r} cannot be greater than {}.".format(name, value, max_))

def validate_integer(value, name=None, range_=None):
	"""
	Validates the specified integer.

	*value* (``int`` or ``long``) is the integer to validate.

	*name* (``str``) optionally is the name to use when an error occurs.

	*range_* (``tuple``) optionally contains: the minumum (``int``) and
	maximum (``int``) values of *value*. The minimum and maximum values
	can be ``None`` for no restriction. Default is ``None`` for
	``(None, None)``.

	Raises an ``Exception`` if *value* is not valid.
	"""
	if not name:
		name = 'value'
	if range_ is not None:
		min_, max_ = range_
	else:
		min_ = None
		max_ = None

	if not isinstance(value, six.integer_types):
		raise TypeError("{}:{!r} is not an integer.".format(name, value))

	if min_ is not None and value < min_:
		raise ValueError("{}:{!r} cannot be less than {}.".format(name, value, min_))
	elif max_ is not None and value > max_:
		raise ValueError("{}:{!r} cannot be greater than {}.".format(name, value, max_))

def validate_sequence(value, name=None, size=None):
	"""
	Validates the specified sequence.

	*value* (**sequence**) is the sequence to validate.

	*name* (``str``) optionally is the name to use when an error occurs.

	*size* (``tuple``) optionally contains: the minimum (``int``) and
	maximum (``int``) lengths of *value*. The minimum and maximum lengths
	can be ``None`` for no restriction. Default is ``None`` for
	``(None, None)``.

	Raises an ``Exception`` if *value* is not valid.
	"""
	if not name:
		name = 'value'
	if size is not None:
		min_, max_ = size
	else:
		min_ = None
		max_ = None

	if not is_sequence(value):
		raise TypeError("{}:{!r} is not a sequence.".format(name, value))

	if min_ is not None and len(value) < min_:
		raise ValueError("{}:{!r} length {} cannot be less than {}.".format(name, value, len(value), min_))
	elif max_ is not None and len(value) > max_:
		raise ValueError("{} length {} cannot be greater than {}.".format(name, len(value), max_))

def validate_string(value, name=None, size=None, startswith=None, values=None):
	"""
	Validates the specified string.

	*value* (**string**) is the string to validate.

	*name* (``str``) optionally is the name to use when an error occurs.

	*size* (``tuple``) optionally contains: the minimum (``int``) and
	maximum (``int``) lengths of *value*. The minimum and maximum lengths
	can be ``None`` for no restriction. Default is ``None`` for
	``(None, None)``.

	*startswith* (**string**) optionally is the string that *value* must
	start with.

	*values* (**container**) optionally contains the set of valid values,
	one of which *value* must be.

	Raises an ``Exception`` if *value* is not valid.
	"""
	if not name:
		name = 'value'
	if size is not None:
		min_, max_ = size
	else:
		min_ = None
		max_ = None

	if not isinstance(value, six.string_types):
		raise TypeError("{}:{!r} is not a string.".format(name, value))

	if min_ is not None and len(value) < min_:
		raise ValueError("{}:{!r} length {} cannot be less than {}.".format(name, value, len(value), min_))
	elif max_ is not None and len(value) > max_:
		raise ValueError("{} length {} cannot be greater than {}.".format(name, len(value), max_))

	if startswith is not None and not value.startswith(startswith):
		raise ValueError("{}:{!r} does not start with {!r}.".format(name, value, startswith))

	if values is not None and value not in values:
		raise LookupError("{}:{!r} is not {}.".format(name, value, ", ".join(map(repr, values))))
