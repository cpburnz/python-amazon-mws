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
	* [Flat-File Feeds](#tab-separated-flat-file-feeds)
		* [Book](#book)
		* [UIEE (Universal Information Exchange Environment) Book](#uiee-universal-information-exchange-environment-book)
		* [Product Converge (Merging)](#products-converge-merging)
		* [Product Data](#product-data)
		* [Product Inventory](#product-inventory)
		* [Product Pricing and Quantities](#product-pricing-and-inventory)
* [Orders](#orders)
* [Products](#products)
* [Reports](#reports)
* [SellersFeeds](#sellersfeeds)

### Feeds

Push data in bulk to your Amazon Marketplace(s) through XML data structures or tab-delimited flat-files.

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
>>> import amazonmws.
>>>	import amazonmws.feeds
>>> import BeautifulSoup # Used to parse resulting XML
>>>	
>>>	ACCESS_KEY   = 'your-access-key'
>>>	SECRET_KEY   = 'your-secret-key'
>>>	MERCHANT_ID  = 'your-merchant-id'
>>>
>>>	# Valid values include: ca, cn, eu, in, jp, us.
>>>	# Note: Marketplaces specified must be enabled on your MWS account.
>>>	ENDPOINTS = ['us']
>>> MARKETPLACES = 
>>>
>>>	feed = amazonmws.feeds.MWSFeeds(ACCESS_KEY, SECRET_KEY, MERCHANT_ID)
>>>
>>> '''
>>> submit_feed() accepts
>>> '''
>>> submit_result = feed.submit_feed()
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

> #### Tab-Separated Flat File Feeds
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
