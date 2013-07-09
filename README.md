# python-amazon-mws

A powerful, easy to use Amazon MWS (Marketplace Web Services) API for Python.

## Documentation

### Table of Contents
* [Introduction](#introduction)
* [Common Arguments](#common-arguments)
	* [marketplaces](#marketplaces)
	* [from_date](#from_date)
	* [to_date](#to_date)
	* [next_token](#next_token)
	* [debug](#debug)
* [Feeds](#feeds)
	* [Common Feed Arguments](#common-feed-arguments)
		* [submissions](#submissions)
		* [feed_types](#feed_types)
		* [statuses](#statuses)
	* [Feed Calls](#feed-calls)
		* [cancel_submissions](#cancel_submissions)
		* [count_submissions](#count_submissions)
		* [get_report](#get_report)
		* [list_submissions](#list_submissions)
		* [list_submissions_next](#list_submissions_next)
		* [submit_feed](#submit_feed)
* [Fulfillment (not yet implemented)](#fulfillment)
	* [Inbound](#inbound)
		* [CreateInboundShipmentPlan](#createinboundshipmentplan)
		* [CreateInboundShipment](#createinboundshipment)
		* [UpdateInboundShipment](#updateinboundshipment)
		* [ListInboundShipments](#listinboundshipments)
		* [ListInboundShipmentsByNextToken](#listinboundshipmentsbynexttoken)
		* [ListInboundShipmentItems](#listinboundshipmentitems)
		* [ListInboundShipmentItemsByNextToken](#listinboundshipmentitemsbynexttoken)
		* [GetServiceStatus](#getservicestatus)
	* [Inventory](#inventory)
		* [ListInventorySupply](#listinventorysupply)
		* [ListInventorySupplyByNextToken](#listinventorysupplybynexttoken)
		* [GetServiceStatus](#getservicestatus-1)
	* [Outbound](#outbound)
		* [GetFulfillmentPreview](#getfulfillmentpreview)
		* [CreateFulfillmentOrder](#createfulfillmentorder)
		* [GetFulfillmentOrder](#getfulfillmentorder)
		* [ListAllFulfillmentOrders](#listallfulfillmentorders)
		* [ListAllFulfillmentOrdersByNextToken](#listallfulfillmentordersbynexttoken)
		* [GetPackageTrackingDetails](#getpackagetrackingdetails)
		* [CancelFulfillmentOrder](#cancelfulfillmentorder)
		* [GetServiceStatus](#getservicestatus-2)
* [Orders](#orders)
	* [Order Calls](#order-calls)
		* [list_orders](#list_orders)
		* [list_orders_next](#list_orders_next)
		* [send_request](#send_request)
* [Products](#products)
	* [Common Product Arguments](#common-product-arguments)
		* [marketplace_id](#marketplace_id)
		* [id_type](#id_type)
		* [id_list](#id_list)
		* [verbose](#verbose)
		* [condition](#condition)
	* [Product Calls](#product-calls)
		* [get_categories](#get_categories)
		* [get_competitive_pricing](#get_competitive_pricing)
		* [get_lowest_listings](#get_lowest_listings)
		* [get_my_price](#get_my_price)
		* [get_products](#get_products)
		* [list_matching](#list_matching)
* [Recommendations (not yet implemented)](#recommendations)
	* [GetLastUpdatedTimeForRecommendations](#getlastupdatedtimeforrecommendations)
	* [ListRecommendations / ListRecommendationsByNextToken](#listrecommendations--listrecommendationsbynexttoken)
* [Reports](#reports)
	* [Common Report Arguments](#common-report-arguments)
		* [requests](#requests)
		* [report_types](#report_types)
		* [statuses](#statuses-1)
		* [acknowledged](#acknowledged)
		* [max_count](#max_count)
	* [Report Calls](#report-calls)
		* [cancel_report_requests](#cancel_report_requests)
		* [get_report](#get_report-1)
		* [get_report_count](#get_report_count)
		* [get_report_list](#get_report_list)
		* [get_report_list_next](#get_report_list_next)
		* [get_report_request_count](#get_report_request_count)
		* [get_report_request_list](#get_report_request_list)
		* [get_report_request_list_next](#get_report_request_list_next)
		* [get_report_schedule_count (not yet implemented)](#get_report_schedule_count)
		* [get_report_schedule_list (not yet implemented)](#get_report_schedule_list)
		* [get_report_schedule_list_next (not yet implemented)](#get_report_schedule_list_next)
		* [manage_report_schedule (not yet implemented)](#manage_report_schedule)
		* [request_report](#request_report)
		* [update_report_acknowledgements](#update_report_acknowledgements)
* [Sellers](#sellers)
	* [Seller Calls](#seller-calls)
		* [get_status](#get_status)
		* [list_marketplaces](#list_marketplaces)
		* [list_marketplaces_next](#list_marketplaces_next)

### Introduction
> 
> TODO: Add introduction.
> 

### Common Arguments
> 
> #### marketplaces
> 
>> TODO: Add documentation.
> 
> #### from_date
> 
>> TODO: Add documentation.
> 
> #### to_date
> 
>> TODO: Add documentation.
> 
> #### next_token
> 
>> TODO: Add documentation.
> 
> #### debug
> 
>> TODO: Add documentation.

### Feeds
> 
> #### Common Feed Arguments
> 
>> 
>> ##### submissions
>> 
>>> TODO: Add documentation.
>> 
>> ##### feed_types
>> 
>>> TODO: Add documentation.
>> 
>> ##### statuses
>> 
>>> TODO: Add documentation.
> 
> #### Feed Calls
> 
>> 
>> ##### cancel_submissions
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### count_submissions
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### list_submissions
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### list_submissions_next
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### submit_feed
>> 
>>> TODO: Add documentation/examples.

### Fulfillment
> 
> Fulfillment has not yet been implemented into this API.
> 
> ### Inbound
> 
> Inbound has not yet been implemented into this API.
> 
> Inbound Calls:
>> 
>> #### CreateInboundShipmentPlan
>> 
>> #### CreateInboundShipment
>> 
>> #### UpdateInboundShipment
>> 
>> #### ListInboundShipments
>> 
>> #### ListInboundShipmentsByNextToken
>> 
>> #### ListInboundShipmentItems
>> 
>> #### ListInboundShipmentItemsByNextToken
>> 
>> #### GetServiceStatus
>> 
> 
> ### Inventory
> 
> Inventory has not yet been implemented into this API.
> 
> Inventory Calls:
>> #### ListInventorySupply
>> #### ListInventorySupplyByNextToken
>> #### GetServiceStatus
> 
> ### Outbound
> 
> Outbound has not yet been implemented into this API.
> 
> Outbound Calls:
>> 
>> #### GetFulfillmentPreview
>> 
>> #### CreateFulfillmentOrder
>> 
>> #### GetFulfillmentOrder
>> 
>> #### ListAllFulfillmentOrders
>> 
>> #### ListAllFulfillmentOrdersByNextToken
>> 
>> #### GetPackageTrackingDetails
>> 
>> #### CancelFulfillmentOrder
>> 
>> #### GetServiceStatus
>> 

### Orders
> #### Order Calls
> 
>> 
>> ##### list_orders
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### list_orders_next
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### send_request
>> 
>>> TODO: Add documentation/examples.

### Products
> 
> #### Common Product Arguments
> 
>> 
>> ##### marketplace_id
>> 
>>> TODO: Add documentation.
>> 
>> ##### id_type
>> 
>>> TODO: Add documentation.
>> 
>> ##### id_list
>> 
>>> TODO: Add documentation.
>> 
>> ##### verbose
>> 
>>> TODO: Add documentation.
>> 
>> ##### condition
>> 
>>> TODO: Add documentation.
> 
> #### Product Calls
> 
>> 
>> ##### get_categories
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_competitive_pricing
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_lowest_listings
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_my_price
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_products
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### list_matching
>> 
>>> TODO: Add documentation/examples.

### Recommendations
> 
> Recommendations has not yet been implemented into this API.
> 
> Recommendations Calls:
>> 
>> #### GetLastUpdatedTimeForRecommendations
>> 
>> #### ListRecommendations
>> 
>> #### ListRecommendationsByNextToken
>> 

### Reports

> 
> #### Common Report Arguments
> 
>> 
>> ##### requests
>> 
>>> TODO: Add documentation.
>> 
>> ##### report_types
>> 
>>> TODO: Add documentation.
>> 
>> ##### statuses
>> 
>>> TODO: Add documentation.
>> 
>> ##### acknowledged
>> 
>>> TODO: Add documentation.
>> 
>> ##### max_count
>> 
>>> TODO: Add documentation.
> 
> #### Report Calls
> 
>> 
>> ##### cancel_report_requests
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_count
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_list
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_list_next
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_request_count
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_request_list
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_request_list_next
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_schedule_count
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_schedule_list
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### get_report_schedule_list_next
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### manage_report_schedule
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### request_report
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### update_report_acknowledgements
>> 
>>> TODO: Add documentation/examples.

### Sellers
> #### Seller Calls
> 
>> 
>> ##### get_status
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### list_marketplaces
>> 
>>> TODO: Add documentation/examples.
>> 
>> ##### list_marketplaces_next
>> 
>>> TODO: Add documentation/examples.
