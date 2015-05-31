from django.http import *
from enum import Enum
import simplejson

IMAGECHOICE = (
	('c', 'Compaction'),
	('m', 'Moisture'),
	('t', 'Transpiration'),
)

class MESSAGE(Enum):
	s = 'Success'
	f = 'Fail'

http_response = {
	'Success': HttpResponse,
	'Fail': HttpResponseServerError,
}

def generateHTTPResponse(function, key):
	result = {}
	result[key] = function

	return http_response[key](simplejson.dumps(result))

def getWSLParameter():
	return (2.86, -1.96)

def getSVPParameter():
	t_svp = list(range(0,42,1))
	p_svp = [611, 657, 706, 758, 813, 872, 935, 1002, 1073, 1148, 1228, 1312, 1402, 1497, 1598, 1705, 1818, 1937, 2064, 2197, 2338, 2486, 2643, 2809, 2983, 3167, 3361, 3565, 3779, 4005, 4242, 4492, 4754, 5029, 5318, 5621, 5940, 6273, 6623, 6990, 7374, 7776]
	return (t_svp, p_svp)

def getDatetimeFormat():
	return ('%Y-%m-%d %H:%M:%S')

def getDateFormat():
	return ('%Y-%m-%d')

def getWidthPixelNum():
	return 512

def getImpoDataMax(x):
	return {
        'transpiration': 20,
        'moisture': 30,
    }[x]

def getImpoDataMin(x):
	return{
		'transpiration': 50,
		'moisture': 60,
	}[x]