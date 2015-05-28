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

* Date Format: yyyy-MM-dd hh:mm:ss
* Http Response Format: JSON


#### APIs


/farm/testnetwork
/farm/newsample
/farm/getdata
/farm/getdetail
/farm/gethistory
/farm/getimpodata

