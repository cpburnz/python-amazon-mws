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
* [Orders](#orders)
* [Products](#products)
* [Reports](#reports)
* [SellersFeeds](#sellersfeeds)

### Feeds

Push data in bulk to your Amazon Marketplace(s) through XML data structures or tab-delimited flat-files.

> #### XML Feeds
>> All feeds are submitted through a common interface.
>> 
>> In all examples within this section, prepend the following code:
>> ```python
>> import amazonmws.mws
>> import amazonmws.feeds
>> import BeautifulSoup # Used to parse XML response
>> 
>> # Specify your AWS authentication credentials:
>> ACCESS_KEY  = 'your-access-key'
>> SECRET_KEY  = 'your-secret-key'
>> MERCHANT_ID = 'your-merchant-id'
>>
# Specify the endpoint the feed will be submitted to. May be the name of an
# endpoint, or an actual URL. Valid endpoints names include:
#	- ca, cn, eu, in, jp, us.
>> ENDPOINT = 'us' # must be a string
>> 
>> # Instantiate the feeds object
>> feed = amazonmws.feeds.MWSFeeds(ACCESS_KEY, SECRET_KEY, MERCHANT_ID, ENDPOINT)
>> ```
>> ##### Offers
>>> TODO: Overview and examples

>> ##### Order Acknowledgement
>>> TODO: Overview and examples

>> ##### Order Cancellation
>>> TODO: Overview and examples

>> ##### Order Fulfillment
>>> TODO: Overview and examples

>> ##### Product Data

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
