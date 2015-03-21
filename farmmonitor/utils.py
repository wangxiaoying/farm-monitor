from django.http import HttpResponse
from enum import Enum
import simplejson

IMAGECHOICE = (
    ('m', 'Moisture'),
    ('t', 'Transpiration'),
    ('n', 'Normal'),
)

class MESSAGE(Enum):
	s = 'Success'
	f = 'Fail'
	fg = 'Grid Not Exist'

def generateHTTPResponse(message, key="result"):
	result = {}
	result[key] = message
	return HttpResponse(simplejson.dumps(result))
