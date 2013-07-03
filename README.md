# python-amazon-mws

A powerful, easy to use Amazon MWS (Marketplace Web Services) API for Python.

## Documentation

### Table of Contents
* [Feeds](#feeds)
	* [Submitting a Feed](#submitting-a-feed)
		* [Setting up a Feed](#setting-up-a-feed)
		* [Example XML Response](#example-xml-response)
		* [Complete Example](#complete-example)
	* [Reporting on a Submitted Feed](#reporting-on-a-submitted-feed)
		* [Requesting the Report on a Feed](#requesting-the-report-on-a-feed)
		* [Example XML Responses](#example-xml-responses)
			* [Error Response: Feed Processing Result Not Ready](#error-response-feed-processing-result-not-ready)
			* [Error Response: Invalid Feed Submission ID](#error-response-invalid-feed-submission-id)
			* [Error Response: Invalid Request](#error-response-invalid-request)
			* [Successful Response](#successful-response)
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

### Feeds
> Push data in bulk to your Amazon Marketplace(s) through the submission of XML data structures or tab-delimited flat-files.
> 
> Amazon MWS breaks up Feeds into two steps:
> 
> 1. Submit the Feed: Amazon MWS will return a response containing a Feed Submission ID, which you will want to store to later report on the results of the submitted feed. Amazon MWS asynchronously processes the request, which can take anywhere from a minute to an hour or more.
> 2. Report on the Feed: The results of the feed will not be available until the submitted feed has been completely processed. If you request a report on a feed which has not yet completed processing, you'll receive an error stating so. When the feed has completed processing, you'll receive a tab-delimited response containing information on the submitted feed including successful/unsuccessful counts, and details on any warnings or errors that were encountered.
> 
> #### Submitting a Feed
> 
>> All feeds are submitted through an instance of `MWSFeeds` by calling and passing arguments to `submit_feed()`.
>> 
>> ##### Setting up a Feed
>> 
>>> ```python
>>> import amazonmws.mws
>>> import amazonmws.feeds
>>> import BeautifulSoup # Used to parse XML response from MWS feed submission
>>> 
>>> # Specify your AWS authentication credentials:
>>> ACCESS_KEY  = 'your-access-key'
>>> SECRET_KEY  = 'your-secret-key'
>>> MERCHANT_ID = 'your-merchant-id'
>>> 
>>> # Specify which parts of the request we wish to debug, by setting keys on a
>>> # dictionary. If the debug argument is omitted or set to None, defaults to
>>> # no debugging. Valid debugging keys:
>>> #	- body, info, url
>>> DEBUG = { # In our example, we'll enable all debugging:
>>> 	'body': True,
>>> 	'info': True,
>>> 	'url':  True,
>>> }
>>>  
>>> # Specify the endpoint the feed will be submitted to. Can be the name of an
>>> # endpoint, or an actual URL. Valid endpoint names include:
>>> #	- ca, cn, eu, in, jp, us.
>>> ENDPOINT = 'us' # must be a string
>>> 
>>> # Specify the Marketplaces you wish to interface with. You may specify the
>>> # Marketplace IDs manually, or you can reference them by their ISO-2 country
>>> # code via amazonmws.mws.MARKETPLACE_IDS. When referencing through an ISO-2
>>> # country code, valid marketplace names include:
>>> #	- ca, cn, in, jp, us, de, es, fr, it, uk
>>> # If marketplaces is omitted as an argument or when set to None, defaults to all
>>> # marketplaces.
>>> MARKETPLACE_IDS = [
>>> 	amazonmws.mws.MARKETPLACE_IDS['us'], # United States  (returns "ATVPDKIKX0DER")
>>> 	amazonmws.mws.MARKETPLACE_IDS['ca'], # Canada         (returns "A2EUQ1WTGCTBG2")
>>> 	'A1F83G8C2ARO7P'                     # United Kingdom (specified directly)
>>> ]
>>> 
>>> # Instantiate the feeds object.
>>> feed = amazonmws.feeds.MWSFeeds(ACCESS_KEY, SECRET_KEY, MERCHANT_ID, ENDPOINT)
>>> 
>>> # Load the feed we're going to push to MWS. Feeds may be passed as strings, or
>>> # as file pointers. In this example we're going to use a file pointer.
>>> feed_fp = open('/path/to/my/feed')
>>> ```
>> 
>> ##### Example XML Response
>> 
>>> ```xml
>>> <?xml version='1.0' encoding='utf-8'?>
>>> <submitfeedresponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
>>> 	<submitfeedresult>
>>> 		<feedsubmissioninfo>
>>> 			<feedsubmissionid>1234567890</feedsubmissionid>
>>> 			<feedtype>_POST_FLAT_FILE_LISTINGS_DATA_</feedtype>
>>> 			<submitteddate>2013-01-01T01:01:01+00:00</submitteddate>
>>> 			<feedprocessingstatus>_SUBMITTED_</feedprocessingstatus>
>>> 		</feedsubmissioninfo>
>>> 	</submitfeedresult>
>>> 	<responsemetadata>
>>> 		<requestid>1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d</requestid>
>>> 	</responsemetadata>
>>> </submitfeedresponse>
>>> ```
>> 
>> ##### Complete Example
>> 
>>> Here is a full example of what a Feed submission may look like, including the extraction of the Feed Submission ID:
>>> ```python
>>> import amazonmws.mws
>>> import amazonmws.feeds
>>> import BeautifulSoup # Used to parse XML response from MWS feed submission
>>> 
>>> # Specify your AWS authentication credentials:
>>> ACCESS_KEY  = 'your-access-key'
>>> SECRET_KEY  = 'your-secret-key'
>>> MERCHANT_ID = 'your-merchant-id'
>>> 
>>> # Specify which parts of the request we wish to debug, by setting keys on a
>>> # dictionary. If the debug argument is omitted or set to None, defaults to
>>> # no debugging. Valid debugging keys:
>>> #	- body, info, url
>>> DEBUG = { # In our example, we'll enable all debugging:
>>> 	'body': True,
>>> 	'info': True,
>>> 	'url':  True,
>>> }
>>> 
>>> # Specify the endpoint the feed will be submitted to. Can be the name of an
>>> # endpoint, or an actual URL. Valid endpoint names include:
>>> #	- ca, cn, eu, in, jp, us.
>>> ENDPOINT = 'us' # must be a string
>>> 
>>> # Specify the Marketplaces you wish to interface with. You may specify the
>>> # Marketplace IDs manually, or you can reference them by their ISO-2 country
>>> # code via amazonmws.mws.MARKETPLACE_IDS. When referencing through an ISO-2
>>> # country code, valid marketplace names include:
>>> #	- ca, cn, in, jp, us, de, es, fr, it, uk
>>> # If marketplaces is omitted as an argument or when set to None, defaults to all
>>> # marketplaces.
>>> MARKETPLACE_IDS = [
>>> 	amazonmws.mws.MARKETPLACE_IDS['us'], # United States  (returns "ATVPDKIKX0DER")
>>> 	amazonmws.mws.MARKETPLACE_IDS['ca'], # Canada         (returns "A2EUQ1WTGCTBG2")
>>> 	'A1F83G8C2ARO7P'                     # United Kingdom (specified directly)
>>> ]
>>> 
>>> # Instantiate the feeds object.
>>> feed = amazonmws.feeds.MWSFeeds(ACCESS_KEY, SECRET_KEY, MERCHANT_ID, ENDPOINT)
>>> 
>>> # Load the feed we're going to push to MWS. Feeds may be passed as strings, or
>>> # as file pointers. In this example we're going to use a file pointer.
>>> feed_fp = open('/path/to/my/feed')
>>> 
>>> # Specify the feed type, using it's simplified name:
>>> feed_type_name = 'flat_product_data'
>>> 
>>> # Grab the MWS feed type based on the feed type name:
>>> feed_type = amazonmws.feeds.FEED_TYPES[feed_type_name] # Returns: "_POST_FLAT_FILE_LISTINGS_DATA_"
>>> 
>>> # Grab the MWS feed method based on the feed type name:
>>> feed_method = amazonmws.feeds.FEED_METHODS[feed_type_name] # Returns: "flat-file"
>>> 
>>> # Grab the content-type for the feed based on the endpoint and feed method:
>>> content_type = amazonmws.feeds.CONTENT_TYPES[ENDPOINT][feed_method] # Returns: "text/tab-separated-values; charset=iso-8859-1"
>>> 
>>> # Submit the feed to MWS; returns an XML string:
>>> feed_result = feed.submit_feed(feed_type, feed_fp, content_type, marketplaces=MARKETPLACE_IDS, debug=DEBUG)
>>> 
>>> # Load the resulting XML string into your XML parser of choice. In this example
>>> # we'll use BeautifulSoup.
>>> feed_bs = BeautifulSoup.BeautifulSoup(feed_result)
>>> 
>>> # Grab the Feed Submission ID returned by MWS.
>>> try: # Submission was successful (this doesn't necessairily mean there weren't any errors, though!)
>>> 	feed_id = feed_bs('feedsubmissionid')[0].text
>>> 	print 'Submission successful! Record this Feed Submission ID so we can report on the status of the feed after MWS has finished processing it:', feed_id
>>> except Exception, e: # Any error was encountered...
>>> 	print 'ERROR: There was a problem submitting the feed:', e
>>> ```
> 
> #### Reporting on a Submitted Feed
> 
>> Depending on whether or not Amazon MWS has finished processing your feed, you'll receive one of two responses:
>> 
>> ##### Requesting the Report on a Feed
>> 
>>> ```python
>>> import amazonmws.mws
>>> import amazonmws.feeds
>>> import BeautifulSoup # Used to parse XML response
>>> 
>>> # Replace this with your Feed ID:
>>> FEED_ID = 1234567890
>>> 
>>> # Specify your AWS authentication credentials:
>>> ACCESS_KEY  = 'your-access-key'
>>> SECRET_KEY  = 'your-secret-key'
>>> MERCHANT_ID = 'your-merchant-id'
>>> 
>>> # Specify the endpoint the feed will be submitted to. Can be the name of an
>>> # endpoint, or an actual URL. Valid endpoint names include:
>>> #	- ca, cn, eu, in, jp, us.
>>> ENDPOINT = 'us' # must be a string
>>> 
>>> # Specify the Marketplaces you wish to interface with. You may specify the
>>> # Marketplace IDs manually, or you can reference them by their ISO-2 country
>>> # code via amazonmws.mws.MARKETPLACE_IDS. When referencing through an ISO-2
>>> # country code, valid marketplace names include:
>>> #	- ca, cn, in, jp, us, de, es, fr, it, uk
>>> # If marketplaces is omitted as an argument or when set to None, defaults to all
>>> # marketplaces.
>>> MARKETPLACE_IDS = [
>>> 	amazonmws.mws.MARKETPLACE_IDS['us'], # United States  (returns "ATVPDKIKX0DER")
>>> 	amazonmws.mws.MARKETPLACE_IDS['ca'], # Canada         (returns "A2EUQ1WTGCTBG2")
>>> 	'A1F83G8C2ARO7P'                     # United Kingdom (specified directly)
>>> ]
>>> 
>>> # Throw everything in a try/except so we can print debug data if something doesn't
>>> # go right.
>>> try:
>>> 	# Instantiate the feeds object.
>>> 	feed = amazonmws.feeds.MWSFeeds(ACCESS_KEY, SECRET_KEY, MERCHANT_ID, ENDPOINT)
>>> 	
>>> 	# Request a report on the Feed ID specified:
>>> 	feed_report = feed.get_report(feed_id)
>>> 	
>>> 	# Load the resulting XML string into your XML parser of choice. In this example
>>> 	# we use BeautifulSoup.
>>> 	report_bs = BeautifulSoup.BeautifulSoup(feed_report)
>>> 	
>>> 	# Check if an "ErrorResponse" XML tag is present. If it is, we know
>>> 	# the feed isn't done processing, or something else is wrong.
>>> 	if len(report_bs('errorresponse')): # An error was encountered.
>>> 		# Grab error code and message.
>>> 		error_code = report_bs('errorresponse')[0]('error')[0]('code')[0]
>>> 		error_message = report_bs('errorresponse')[0]('error')[0]('message')[0]
>>> 	
>>> 		# Determine the type of error encountered.
>>> 		if error_code == 'FeedProcessingResultNotReady':
>>> 			print 'Feed ID specified isn\'t done processing yet. Request again in a little while.'
>>> 		elif error_code == 'InvalidFeedSubmissionId': # Feed ID specified doesn't exist
>>> 			print 'Feed ID specified doesn\'t exist.'
>>> 		elif error_code == 'InvalidRequest': # Invalid request, possibly a incorrectly formatted Feed ID. Feed IDs will always be integers.
>>> 			print 'Invalid request, maybe an incorrectly formatted Feed ID? Feed IDs will always be integers.'
>>> 		else:
>>> 			print 'Some other error we haven\'t account for was encountered.'
>>>	
>>> 		# For debugging purposes, print the error Code and Message encountered.
>>> 		print '	Error Code:', error_code
>>> 		print '	Error Message:', error_message
>>> 	else: # No error was encountered, this must be our report!
>>> 		print 'Report successful, here\'s your report:
>>> 	 	print feed_report
>>> except Exception, e:
>>> 	print 'An exception has been encountered, here\'s the error:'
>>> 	print e
>>> ```
>> 
>> ##### Example XML Responses
>> 
>>> 
>>> ##### Error Response: Feed Processing Result Not Ready
>>> 
>>>> If a Feed ID passed has not yet finished processing, you'll receive a response similar to the following:
>>>> ```xml
>>>> <?xml version="1.0"?>
>>>> <ErrorResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
>>>> 	<Error>
>>>> 		<Type>Sender</Type>
>>>> 		<Code>FeedProcessingResultNotReady</Code>
>>>> 		<Message>Feed Submission Result is not ready for Feed Submission Id: 7465486170</Message>
>>>> 		<Detail/>
>>>> 	</Error>
>>>> 	<RequestID>1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d</RequestID>
>>>> </ErrorResponse>
>>>> ```
>>> 
>>> ##### Error Response: Invalid Feed Submission ID
>>> 
>>>> If the Feed ID passed does not exist, you'll receive a response similar to the following:
>>>> ```xml
>>>> <?xml version="1.0"?>
>>>> <ErrorResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
>>>> 	<Error>
>>>> 		<Type>Sender</Type>
>>>> 		<Code>InvalidFeedSubmissionId</Code>
>>>> 		<Message>Failed to find feed with Feed Submission ID: 123456789</Message>
>>>> 		<Detail/>
>>>> 	</Error>
>>>> 	<RequestID>1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d</RequestID>
>>>> </ErrorResponse>
>>>> ```
>>> 
>>> ##### Error Response: Invalid Request
>>> 
>>>> If you have supplied an invalid Feed ID (such as a non-numeric value), you'll receive a response similar to the following:
>>>> ```xml
>>>> <?xml version="1.0"?>
>>>> <ErrorResponse xmlns="http://mws.amazonaws.com/doc/2009-01-01/">
>>>> 	<Error>
>>>> 		<Type>Sender</Type>
>>>> 		<Code>InvalidRequest</Code>
>>>> 		<Message>one4567890 failed a validation check: one4567890 is not a valid identifer.</Message>
>>>> 		<Detail/>
>>>> 	</Error>
>>>> 	<RequestID>1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d</RequestID>
>>>> </ErrorResponse>
>>>> ```
>>> 
>>> ##### Successful Response
>>> 
>>>> TODO: Check if Flat-File feed report responses are different than XML feed report responses.
>>>> 
>>>> On successful retrieval of a Feed ID's report, you'll receive a response similar to the following.
>>>> 
>>>> Response is in tab-delimited format, with "\n" for newlines. The end of the file also contains a trailing newline (\n) character. Because the GitHub interface replaces tab characters with spaces, we'll show this example in two separate formats:
>>>> 
>>>> <b>Tab characters replaced with "[tab]":</b>
>>>> ```
>>>> Feed Processing Summary:
>>>> [tab]Number of records processed[tab][tab]1
>>>> [tab]Number of records successful[tab][tab]1
>>>> 
>>>> original-record-number[tab]sku[tab]error-code[tab]error-type[tab]error-message
>>>> 1[tab]728273[tab]99040[tab]Warning[tab]A value was not provided for "main_image_url". Please provide a value for "main_image_url" so the product has an image. Images appear in search results and on the product detail page, and help customers evaluate products.
>>>> 1[tab]728273[tab]99041[tab]Warning[tab]A value was not provided for "bullet_point". Please provide a value for "bullet_point". This information appears on the product detail page and helps customers evaluate products.
>>>> 1[tab]728273[tab]99042[tab]Warning[tab]A value was not provided for "item-type". Please provide a value for "item-type". Please use the Product Classifier or download the category-specific Browse Tree Guide from Seller Help to see a list of valid "item-type" values. This information tells Amazon where your product should be classified and affects how easily customers can find your product.
>>>> 
>>>> ```
>>>> <b>Tab characters left intact (tab characters are replaced with an arbitrary number of spaces when viewed through the GitHub interface):</b>
>>>> ```
>>>> Feed Processing Summary:
>>>> 	Number of records processed		1
>>>> 	Number of records successful		1
>>>> 
>>>> original-record-number	sku	error-code	error-type	error-message
>>>> 1	728273	99040	Warning	A value was not provided for "main_image_url". Please provide a value for "main_image_url" so the product has an image. Images appear in search results and on the product detail page, and help customers evaluate products.
>>>> 1	728273	99041	Warning	A value was not provided for "bullet_point". Please provide a value for "bullet_point". This information appears on the product detail page and helps customers evaluate products.
>>>> 1	728273	99042	Warning	A value was not provided for "item-type". Please provide a value for "item-type". Please use the Product Classifier or download the category-specific Browse Tree Guide from Seller Help to see a list of valid "item-type" values. This information tells Amazon where your product should be classified and affects how easily customers can find your product.
>>>> 
>>>> ```
> 
> #### XML Feeds
> 
>> 
>> ##### Offers
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Order Acknowledgement
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Order Cancellation
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Order Fulfillment
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Data
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Image
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Inventory
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Item
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Override
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Pricing
>>
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Relationship
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Shipping Override
>>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Webstore Item
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
> 
> #### Flat-File Feeds
>> ##### Book
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### UIEE (Universal Information Exchange Environment) Book
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Products Converge (Merging)
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> TODO: Add code example.
>> 
>> ##### Product Data
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> 
>>> ```python
>>> # Specify the feed type, using it's simplified name:
>>> feed_type_name = 'flat_product_data'
>>> 
>>> # Grab the MWS feed type based on the feed type name:
>>> feed_type = amazonmws.feeds.FEED_TYPES[feed_type_name] # Returns: "_POST_FLAT_FILE_LISTINGS_DATA_"
>>> 
>>> # Grab the MWS feed method based on the feed type name:
>>> feed_method = amazonmws.feeds.FEED_METHODS[feed_type_name] # Returns: "flat-file"
>>> 
>>> # Grab the content-type for the feed based on the endpoint and feed method:
>>> content_type = amazonmws.feeds.CONTENT_TYPES[ENDPOINT][feed_method] # Returns: "text/tab-separated-values; charset=iso-8859-1"
>>> 
>>> # Submit the feed to MWS; returns an XML string:
>>> feed_result = feed.submit_feed(feed_type, feed_fp, content_type, marketplaces=MARKETPLACE_IDS, debug=DEBUG)
>>> 
>>> # Load the resulting XML string into your XML parser of choice. In this example
>>> # we'll use BeautifulSoup.
>>> feed_bs = BeautifulSoup.BeautifulSoup(feed_result)
>>> ```
>> 
>> ##### Product Inventory
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> 
>>> ```python
>>> # Specify the feed type, using it's simplified name:
>>> feed_type_name = 'flat_product_inventory'
>>> 
>>> # Grab the MWS feed type based on the feed type name:
>>> feed_type = amazonmws.feeds.FEED_TYPES[feed_type_name] # Returns: "_POST_FLAT_FILE_INVLOADER_DATA_"
>>> 
>>> # Grab the MWS feed method based on the feed type name:
>>> feed_method = amazonmws.feeds.FEED_METHODS[feed_type_name] # Returns: "flat-file"
>>> 
>>> # Grab the content-type for the feed based on the endpoint and feed method:
>>> content_type = amazonmws.feeds.CONTENT_TYPES[ENDPOINT][feed_method] # Returns: "text/tab-separated-values; charset=iso-8859-1"
>>> 
>>> # Submit the feed to MWS; returns an XML string:
>>> feed_result = feed.submit_feed(feed_type, feed_fp, content_type, marketplaces=MARKETPLACE_IDS, debug=DEBUG)
>>> 
>>> # Load the resulting XML string into your XML parser of choice. In this example
>>> # we'll use BeautifulSoup.
>>> feed_bs = BeautifulSoup.BeautifulSoup(feed_result)
>>> ```
>> 
>> ##### Product Pricing & Inventory
>> 
>>> TODO: Add description for this feed.
>>> TODO: Add feed example.
>>> 
>>> ```python
>>> # Specify the feed type, using it's simplified name:
>>> feed_type_name = 'flat_product_price_inv'
>>> 
>>> # Grab the MWS feed type based on the feed type name:
>>> feed_type = amazonmws.feeds.FEED_TYPES[feed_type_name] # Returns: "_POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA_"
>>> 
>>> # Grab the MWS feed method based on the feed type name:
>>> feed_method = amazonmws.feeds.FEED_METHODS[feed_type_name] # Returns: "flat-file"
>>> 
>>> # Grab the content-type for the feed based on the endpoint and feed method:
>>> content_type = amazonmws.feeds.CONTENT_TYPES[ENDPOINT][feed_method] # Returns: "text/tab-separated-values; charset=iso-8859-1"
>>> 
>>> # Submit the feed to MWS; returns an XML string:
>>> feed_result = feed.submit_feed(feed_type, feed_fp, content_type, marketplaces=MARKETPLACE_IDS, debug=DEBUG)
>>> 
>>> # Load the resulting XML string into your XML parser of choice. In this example
>>> # we'll use BeautifulSoup.
>>> feed_bs = BeautifulSoup.BeautifulSoup(feed_result)
>>> ```

### Orders

### Products

### Reports

### SellersFeeds
