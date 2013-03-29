# coding: utf-8
from setuptools import find_packages, setup

from amazonmws import __authors__, __doc__, __license__, __project__, __version__

setup(
	name=__project__,
	version=__version__,
	author=", ".join(__authors__),
	url="https://github.com/cpburnz/python-amazon-mws.git",
	description="Amazon MWS API for Python.",
	long_description=__doc__,
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Topic :: Office/Business",
		"Topic :: Software Development :: Libraries :: Python Modules"
	],
	license=__license__,
	packages=find_packages(),
)
