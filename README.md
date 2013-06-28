# python-amazon-mws

The Amazon MWS (Marketplace Web Services) API for Python

## Documentation

### Table of Contents
* [Feeds](#feeds)
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

> Push data in bulk to your Amazon Marketplace(s) through XML data structures or tab-delimited flat-files.
>
> Please note: When a feed is submitted to MWS, all that will be returned to you is whether or not the feed was accepted (does not mean it was formatted correctly), and the Feed ID associated with that submission. To grab specific details on the feed submitted such as what errors have been encountered within the submission, you'll need to perform a subsequent request to request a [feed submission report](#feed-submission-reporting).
>
> All feeds are submitted through a common interface.
> 
> In any of the examples within this section, prepend the following code:
> ```python
> import amazonmws.mws
> import amazonmws.feeds
> import BeautifulSoup # Used to parse XML response from MWS feed submission
> 
> # Specify your AWS authentication credentials:
> ACCESS_KEY  = 'your-access-key'
> SECRET_KEY  = 'your-secret-key'
> MERCHANT_ID = 'your-merchant-id'
> 
> # Specify whether or not we're in DEBUG mode (prints extra debuging data):
> DEBUG = True
> 
> # Specify the endpoint the feed will be submitted to. Can be the name of an
> # endpoint, or an actual URL. Valid endpoint names include:
> #	- ca, cn, eu, in, jp, us.
> ENDPOINT = 'us' # must be a string
> 
> # Specify the Marketplaces you wish to interface with. You may specify the
> # Marketplace IDs manually, or you can reference them by their ISO-2 country
> # code via amazonmws.mws.MARKETPLACE_IDS. When referencing through an ISO-2
> # country code, valid marketplace names include:
> #	- ca, cn, in, jp, us, de, es, fr, it, uk
> # If marketplaces is omitted as an argument or when set to None, defaults to all
> # marketplaces.
> MARKETPLACE_IDS = [
> 	amazonmws.mws.MARKETPLACE_IDS['us'], # United States  (returns "ATVPDKIKX0DER")
> 	amazonmws.mws.MARKETPLACE_IDS['ca'], # Canada         (returns "A2EUQ1WTGCTBG2")
> 	'A1F83G8C2ARO7P'                     # United Kingdom (specified directly)
> ]
> 
> # Instantiate the feeds object.
> feed = amazonmws.feeds.MWSFeeds(ACCESS_KEY, SECRET_KEY, MERCHANT_ID, ENDPOINT)
> 
> # Load the feed we're going to push to MWS. Feeds may be passed as strings, or
> # as file pointers. In this example we're going to use a file pointer.
> feed_fp = open('/path/to/my/feed')
> ```

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
>>> # Grab the MWS feed type based on it's simplified name:
>>> feed_type = amazonmws.feeds.FEED_TYPES['product_data'] # Returns: "_POST_PRODUCT_DATA_"
>>> # Grab the MWS feed method based on the feed_type:
>>> feed_method = amazonmws.feeds.FEED_METHODS[feed_type] # Returns: "xml"
>>> # Grab the content-type for the feed based on the ENDPOINT and feed_method:
>>> content_type = amazonmws.feeds.CONTENT_TYPES[ENDPOINT][feed_method] # Returns: "text/xml"
>>> 
>>> # Submit the Product Data feed to MWS, returning an XML string:
>>> feed_result = amazonmws.feeds.submit_feed(feed_type, feed_fp, content_type, marketplaces=MARKETPLACE_IDS, debug=DEBUG)
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

> #### Feed Submission Reporting
>> TODO: Overview and examples

### Orders

### Products

### Reports

### SellersFeeds
