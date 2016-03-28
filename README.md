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
>>> 
>>> **Arguments**
>>> * submissions (Feeds: Common Arguments)
>>> * feed_types (Feeds: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * all_submissions (Specific Argument)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### count_submissions
>> 
>>> 
>>> **Arguments**
>>> * feed_types (Feeds: Common Arguments)
>>> * statuses (Feeds: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report
>> 
>>> 
>>> **Arguments**
>>> * submission_id (Specific Argument)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### list_submissions
>> 
>>> 
>>> **Arguments**
>>> * submissions (Feeds: Common Arguments)
>>> * count (Specific Argument)
>>> * feed_types (Feeds: Common Arguments)
>>> * statuses (Feeds: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### list_submissions_next
>> 
>>> 
>>> **Arguments**
>>> * next_token (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### submit_feed
>> 
>>> 
>>> **Arguments**
>>> * feed_type (Specific Argument)
>>> * data (Specific Argument)
>>> * content_type (Specific Argument)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 

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
>>> 
>>> **Arguments**
>>> * created_after (Specific Argument)
>>> * updated_after (Specific Argument)
>>> * order_statuses (Specific Argument)
>>> * marketplaces (Common Arguments)
>>> 
>> 
>> ##### list_orders_next
>> 
>>> 
>>> **Arguments**
>>> * next_token (Common Arguments)
>>> 
>> 
>> ##### send_request
>> 
>>> 
>>> **Arguments**
>>> * action (Specific Argument)
>>> * args_dict (Specific Argument)
>>> 

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
>>> 
>>> **Arguments**
>>> * marketplace_id (Products: Common Arguments)
>>> * id_type (Products: Common Arguments)
>>> * id_list (Products: Common Arguments)
>>> * verbose (Products: Common Arguments)
>>> 
>> 
>> ##### get_competitive_pricing
>> 
>>> 
>>> **Arguments**
>>> * marketplace_id (Products: Common Arguments)
>>> * id_type (Products: Common Arguments)
>>> * id_list (Products: Common Arguments)
>>> * verbose (Products: Common Arguments)
>>> 
>> 
>> ##### get_lowest_listings
>> 
>>> 
>>> **Arguments**
>>> * marketplace_id (Products: Common Arguments)
>>> * id_type (Products: Common Arguments)
>>> * id_list (Products: Common Arguments)
>>> * condition (Products: Common Arguments)
>>> * exclude_me (Specific Argument)
>>> * verbose (Products: Common Arguments)
>>> 
>> 
>> ##### get_my_price
>> 
>>> 
>>> **Arguments**
>>> * marketplace_id (Products: Common Arguments)
>>> * id_type (Products: Common Arguments)
>>> * id_list (Products: Common Arguments)
>>> * condition (Products: Common Arguments)
>>> * verbose (Products: Common Arguments)
>>> 
>> 
>> ##### get_products
>> 
>>> 
>>> **Arguments**
>>> * marketplace_id (Products: Common Arguments)
>>> * id_type (Products: Common Arguments)
>>> * id_list (Products: Common Arguments)
>>> * verbose (Products: Common Arguments)
>>> 
>> 
>> ##### list_matching
>> 
>>> 
>>> **Arguments**
>>> * marketplace_id (Products: Common Arguments)
>>> * query (Specific Argument)
>>> * context (Specific Argument)
>>> * verbose (Products: Common Arguments)
>>> 

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
>>> 
>>> **Arguments**
>>> * requests (Reports: Common Arguments)
>>> * report_types (Reports: Common Arguments)
>>> * statuses (Reports: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report
>> 
>>> 
>>> **Arguments**
>>> * report_id (Specific Argument)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report_count
>> 
>>> 
>>> **Arguments**
>>> * report_types (Reports: Common Arguments)
>>> * acknowledged (Reports: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report_list
>> 
>>> 
>>> **Arguments**
>>> * requests (Reports: Common Arguments)
>>> * max_count (Reports: Common Arguments)
>>> * report_types (Reports: Common Arguments)
>>> * acknowledged (Reports: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report_list_next
>> 
>>> 
>>> **Arguments**
>>> * next_token (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report_request_count
>> 
>>> 
>>> **Arguments**
>>> * report_types (Reports: Common Arguments)
>>> * statuses (Reports: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report_request_list
>> 
>>> 
>>> **Arguments**
>>> * requests (Reports: Common Arguments)
>>> * max_count (Reports: Common Arguments)
>>> * report_types (Reports: Common Arguments)
>>> * statuses (Reports: Common Arguments)
>>> * from_date (Common Arguments)
>>> * to_date (Common Arguments)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report_request_list_next
>> 
>>> 
>>> **Arguments**
>>> * next_token (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### get_report_schedule_count
>> 
>>> Not yet implemented within this API.
>> 
>> ##### get_report_schedule_list
>> 
>>> Not yet implemented within this API.
>> 
>> ##### get_report_schedule_list_next
>> 
>>> Not yet implemented within this API.
>> 
>> ##### manage_report_schedule
>> 
>>> Not yet implemented within this API.
>> 
>> ##### request_report
>> 
>>> 
>>> **Arguments**
>>> * report_type (Specific Argument)
>>> * start_date (Specific Argument)
>>> * end_date (Specific Argument)
>>> * show_sales_channel (Specific Argument)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### update_report_acknowledgements
>> 
>>> 
>>> **Arguments**
>>> * reports (Specific Argument)
>>> * marketplaces (Common Arguments)
>>> * debug (Common Arguments)
>>> 

### Sellers
> #### Seller Calls
> 
>> 
>> ##### get_status
>> 
>>> 
>>> **Arguments**
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### list_marketplaces
>> 
>>> 
>>> **Arguments**
>>> * debug (Common Arguments)
>>> 
>> 
>> ##### list_marketplaces_next
>> 
>>> 
>>> **Arguments**
>>> * next_token (Common Arguments)
>>> * debug (Common Arguments)
>>> 
