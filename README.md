# Farm Monitor Server

## Environment

#### Development

* Mac OS X 10.10.3
* Python 3.4.2
* Django 1.6.0
* Mysql: Ver 14.14 Distrib 5.6.22


#### Deployment

* Linux Ubuntu 14.04.1 LTS
* Python 3.4.0
* Django 1.6.0
* Ver 14.14 Distrib 5.5.41
* Host Name: film.h1994st.com
* Port Number: 8899

#### Packages

* pymysql
* simplejson
* numpy
* scipy



## Database Model

Field         | Type         | Remark 					   | Description
------ 		  | ------ 		 | ------ 					   | ------
id            | int(11)      | primary key, auto_increment | point identification		
longtitude    | decimal(9,4) |                     		   | longtitued of the point
latitude      | decimal(9,4) |                     		   | latitude of the point
moisture      | decimal(4,1) |                     		   | soil moisture of the point
air_temp      | decimal(4,1) |                     		   | air temperature of the point
leaf_temp     | decimal(4,1) |                     		   | leaf temperature of the point
humidity      | decimal(4,1) |                     		   | humidity of the point
transpiration | decimal(5,2) |                     		   | calculated by air_temp, leaf_temp and humidity
photo         | varchar(100) |                     		   | url of the photo
time          | datetime     |                     		   | time of acquisition



## API Reference

#### Global Rules

* DateTime Format: yyyy-MM-dd hh:mm:ss
* Http Response Format: JSON


#### APIs

* TestHttpConnection
	* Method: ```POST```
	* HTTP request: ```/farm/testnetwork```
	* Parameters:
		* __message__: _text string_ 
		* __photo__: _file picture_
	* Description:	test network connection
	* Return:
		* Success
			* __Success__: _TestHttpConnection_
		* Failed
			* __Fail__: _TestHttpConnection_

* NewSample
	* Method: ```POST```
	* HTTP request: ```/farm/newsample```
	* Parameters:
		* __longtitude__: _text number ±xxx.xxxx_ 
		* __latitude__: _text numer ±xx.xxxx_
		* __moisture__: _text number ±xxx.x_
		* __transpiration__: _text number ±xxx.xx_
		* __air_temp__: _text number ±xxx.x_
		* __leaf_temp__: _text number ±xxx.x_
		* __humidity__: _text number ±xxx.x_
		* __datetime__: _text datetime_
		* __photo__: _file picture_
	* Description: update new sample
	* Return:
		* Success
			* __Success__: NewSample
		* Failed
			* __Fail__: NewSample

* GetDataPoints
	* Method: ```GET```
	* HTTP request: ```/farm/getdata```
	* Parameters:
	* Description: get recent samples(in 2 days or nearest 20 points)
	* Return:
		* Success
			* __Success__: NewSample
		* Failed
			* __Fail__: NewSample

* GetPointDetail
	* Method: ```GET```
	* HTTP request: ```/farm/getdetail```
	* Parameters:
		* __id__: _text number integer >0_
	* Description: get point detail by id
	* Return
		* Success
			* __longtitude__: _text number ±xxx.xxxx_ 
			* __latitude__: _text numer ±xx.xxxx_
			* __moisture__: _text number ±xxx.x_
			* __transpiration__: _text number ±xxx.xx_
			* __air_temp__: _text number ±xxx.x_
			* __leaf_temp__: _text number ±xxx.x_
			* __humidity__: _text number ±xxx.x_
			* __datetime__: _text datetime_
			* __photo__: _file picture_
		* Failed
			* __Fail__: GetPointDetail

* GetHistoryData
	* Method: ```GET```
	* HTTP request: ```/farm/gethistory```
	* Parameters:
		* __time_from__: _text datetime_
		* __time_to__: _text datetime_
	* Description: get points in a time range(if no points in this range, return nearest 20 points)
	* Return
		* Success
			* __longtitude__: _text number ±xxx.xxxx_ 
			* __latitude__: _text numer ±xx.xxxx_
			* __moisture__: _text number ±xxx.x_
			* __transpiration__: _text number ±xxx.xx_
			* __air_temp__: _text number ±xxx.x_
			* __leaf_temp__: _text number ±xxx.x_
			* __humidity__: _text number ±xxx.x_
			* __datetime__: _text datetime_
			* __photo__: _file picture_
		* Failed
			* __Fail__: _GetHistoryData_

* GetImportantData
	* Method: ```GET```
	* HTTP request: ```/farm/getimpodata```
	* Parameters:
	* Description: get recent issues points
	* Return
		* Success
			* __longtitude__: _text number ±xxx.xxxx_ 
			* __latitude__: _text numer ±xx.xxxx_
			* __moisture__: _text number ±xxx.x_
			* __transpiration__: _text number ±xxx.xx_
			* __air_temp__: _text number ±xxx.x_
			* __leaf_temp__: _text number ±xxx.x_
			* __humidity__: _text number ±xxx.x_
			* __datetime__: _text datetime_
			* __photo__: _file picture_
		* Failed
			* __Fail__: _GetImportantData_

