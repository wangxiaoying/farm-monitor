from django.http import HttpResponse
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

def generateHTTPResponse(message, key="result"):
	result = {}
	result[key] = message
	return HttpResponse(simplejson.dumps(result))
