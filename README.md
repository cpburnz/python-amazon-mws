# python-amazon-mws

The Amazon MWS (Marketplace Web Services) API for Python

## Documentation

### Table of Contents
* [Feeds](#feeds)
	* [Submitting a Feed](#submitting-a-feed)
	* [Reporting on a Submitted Feed](#reporting-on-a-submitted-feed)
	* [XML Feeds](#xml-feeds)
		* [Offers](#offers)
		* [Order Acknowledgement](#order-acknowledgement)
		* [Order Cancellation](#order-cancellation)
		* [Order Fulfillment](#order-fulfillment)
		* [Product Data](#product-data)
		* [Product Image](#product-image)
		* [Product Inventory](#product-inventory)
		* [Product Item](#product-item)
		* [Product Override](#product-override)
		* [Product Pricing](#product-pricing)
		* [Product Relationship](#product-relationship)
		* [Shipping Override](#shipping-override)
		* [Webstore Item](#webstore-item)
	* [Flat-File Feeds](#flat-file-feeds)
		* [Book](#book)
		* [UIEE (Universal Information Exchange Environment) Book](#uiee-universal-information-exchange-environment-book)
		* [Product Converge (Merging)](#products-converge-merging)
		* [Product Data](#product-data-1)
		* [Product Inventory](#product-inventory-1)
		* [Product Pricing and Quantities](#product-pricing--inventory)
	* [Feed Submission Reporting](#feed-submission-reporting)
* [Orders](#orders)
* [Products](#products)
* [Reports](#reports)
* [SellersFeeds](#sellersfeeds)

> ### Feeds
> Push data in bulk to your Amazon Marketplace(s) through XML data structures or tab-delimited flat-files.
> 
> Please note: When a feed is submitted to MWS, all that will be returned to you is whether or not the feed was accepted (does not mean it was formatted correctly), and the Feed ID associated with that submission. To grab specific details on the feed submitted such as what errors have been encountered within the submission, you'll need to perform a subsequent request to grab a [feed submission report](#reporting-on-a-submitted-feed).

> #### Submitting a Feed
>> All feeds are submitted through a common interface.
>> 
>> In any of the examples within this section, prepend the following code:
>> ```python
>> import amazonmws.mws
>> import amazonmws.feeds
>> import BeautifulSoup # Used to parse XML response from MWS feed submission
>> 
>> # Specify your AWS authentication credentials:
>> ACCESS_KEY  = 'your-access-key'
>> SECRET_KEY  = 'your-secret-key'
>> MERCHANT_ID = 'your-merchant-id'
>> 
>> # Specify which parts of the request we wish to debug, by setting keys on a
>> # dictionary. If the debug argument is omitted or set to None, defaults to
>> # no debugging. Valid debugging keys:
>> #	- body, info, url
>> DEBUG = { # In our example, we'll enable all debugging:
>> 	'body': True,
>> 	'info': True,
>> 	'url':  True,
>> }
>> # For no debugging, un-comment the following line:
>> #DEBUG = Nne
>> 
>> # Specify the endpoint the feed will be submitted to. Can be the name of an
>> # endpoint, or an actual URL. Valid endpoint names include:
>> #	- ca, cn, eu, in, jp, us.
>> ENDPOINT = 'us' # must be a string
>> 
>> # Specify the Marketplaces you wish to interface with. You may specify the
>> # Marketplace IDs manually, or you can reference them by their ISO-2 country
>> # code via amazonmws.mws.MARKETPLACE_IDS. When referencing through an ISO-2
>> # country code, valid marketplace names include:
>> #	- ca, cn, in, jp, us, de, es, fr, it, uk
>> # If marketplaces is omitted as an argument or when set to None, defaults to all
>> # marketplaces.
>> MARKETPLACE_IDS = [
>> 	amazonmws.mws.MARKETPLACE_IDS['us'], # United States  (returns "ATVPDKIKX0DER")
>> 	amazonmws.mws.MARKETPLACE_IDS['ca'], # Canada         (returns "A2EUQ1WTGCTBG2")
>> 	'A1F83G8C2ARO7P'                     # United Kingdom (specified directly)
>> ]
>> 
>> # Instantiate the feeds object.
>> feed = amazonmws.feeds.MWSFeeds(ACCESS_KEY, SECRET_KEY, MERCHANT_ID, ENDPOINT)
>> 
>> # Load the feed we're going to push to MWS. Feeds may be passed as strings, or
>> # as file pointers. In this example we're going to use a file pointer.
>> feed_fp = open('/path/to/my/feed')
>> ```

> #### Reporting on a Submitted Feed
>> All feed reports are requested through a common interface.
>> 
>> In any of the examples within this section, append the following code:
>> ```python
>> import time
>> while True: # TODO: Need to test this to ensure it doesn't infinitely loop.
>> 	report_result = feed.get_report(feed_id)
>> 
>> 	# Load the resulting XML string into your XML parser of choice. In this example
>> 	# we'll use BeautifulSoup.
>> 	report_bs = BeautifulSoup.BeautifulSoup(report_result)
>> 
>> 	# Check if MWS has finished parsing our feed:
>> 	if len(report_bs('errorresponse'):
>> 		# MWS hasn't finished parsing our feed yet, let's wait a bit then try again.
>> 		time.wait(10) # Wait 10 seconds.
>> 		continue
>> 	
>> 	# Looks like our feed has finished parsing, let's look at the results:
>> 	break
>> print report_result
>> # TODO: Look at the results.
>> ```

> #### XML Feeds

>> ##### Offers
>>> TODO: Overview and examples

>> ##### Order Acknowledgement
>>> TODO: Overview and examples

>> ##### Order Cancellation
>>> TODO: Overview and examples

>> ##### Order Fulfillment
>>> TODO: Overview and examples

>> ##### Product Data
>>> ```python
>>> # Specify the feed type, using it's simplified name:
>>> feed_type_name = 'product_data'
>>> # Grab the MWS feed type based on the feed type name:
>>> feed_type = amazonmws.feeds.FEED_TYPES[feed_type_name] # Returns: "_POST_PRODUCT_DATA_"
>>> # Grab the MWS feed method based on the feed type name:
>>> feed_method = amazonmws.feeds.FEED_METHODS[feed_type_name] # Returns: "xml"
>>> # Grab the content-type for the feed based on the endpoint and feed method:
>>> content_type = amazonmws.feeds.CONTENT_TYPES[ENDPOINT][feed_method] # Returns: "text/xml"
>>> 
>>> # Submit the feed to MWS; returns an XML string:
>>> feed_result = feed.submit_feed(feed_type, feed_fp, content_type, marketplaces=MARKETPLACE_IDS, debug=DEBUG)
>>> 
>>> # Load the resulting XML string into your XML parser of choice. In this example
>>> # we'll use BeautifulSoup.
>>> feed_bs = BeautifulSoup.BeautifulSoup(feed_result)
>>> ```

>> ##### Product Image
>>> TODO: Overview and examples

>> ##### Product Inventory
>>> TODO: Overview and examples

>> ##### Product Item
>>> TODO: Overview and examples

>> ##### Product Override
>>> TODO: Overview and examples

>> ##### Product Pricing
>>> TODO: Overview and examples

>> ##### Product Relationship
>>> TODO: Overview and examples

>> ##### Shipping Override
>>> TODO: Overview and examples

>> ##### Webstore Item
>>> TODO: Overview and examples

> #### Flat-File Feeds

>>##### Book
>>> TODO: Overview and examples

>> ##### UIEE (Universal Information Exchange Environment) Book
>>> TODO: Overview and examples

>> ##### Products Converge (Merging)
>>> TODO: Overview and examples

>> ##### Product Data
>>> TODO: Overview and examples

>> ##### Product Inventory
>>> TODO: Overview and examples

>> ##### Product Pricing & Inventory
>>> TODO: Overview and examples

### Orders

### Products

### Reports

### SellersFeeds
