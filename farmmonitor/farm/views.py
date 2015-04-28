from django.shortcuts import render
from farm.models import *
from farm.forms import *
from django.views.decorators.csrf import csrf_exempt

import time
import simplejson
import numpy as np
from datetime import datetime, timedelta
from scipy import interpolate

from utils import *

@csrf_exempt
def NewSample(request):
	try:
		longtitude = request.POST.get('longtitude')
		latitude = request.POST.get('latitude')
		moisture = float(request.POST.get('moisture'))
		transpiration = float(request.POST.get('transpiration'))
		air_temp = float(request.POST.get('air_temp'))
		leave_temp = float(request.POST.get('leave_temp'))
		humidity = float(request.POST.get('humidity'))

		date_time = time.strptime(request.POST.get('datetime'), '%m.%d.%Y %H%M.%S')
		dt = datetime.fromtimestamp(time.mktime(date_time))

		# transpiration = __Get_Transpiration(leave_temp, air_temp, humidity)

		new_sample = Sample(longtitude=longtitude, latitude=latitude, moisture=moisture,
			air_temp=air_temp, leave_temp=leave_temp, humidity=humidity, transpiration=transpiration, time=dt)
		new_sample.save()

		form = PhotoForm(request.POST, request.FILES)
		photo = None
		if form.is_valid():
			photo = request.FILES['photo']
			if photo is not None:
				new_sample.photo = photo
				new_sample.save()

		return generateHTTPResponse(MESSAGE.s.value)
	except Exception as e:
		print('Exception NewSample', e)
		return generateHTTPResponse(MESSAGE.f.value)


@csrf_exempt
def TestHttpConnection(request):
	try:
		msg = float(request.POST.get('message'))
		print ('Message', msg)
		form = PhotoForm(request.POST, request.FILES)
		photo = None
		if form.is_valid():
			photo = request.FILES['photo']
			if photo is not None:
				print ('photo success!!!')

		new_test = NetworkTest(message=msg, photo=photo)
		new_test.save()
			
		return generateHTTPResponse(MESSAGE.s.value)
	except Exception as e:
		print('Exception TestHttpConnection', e)
		return generateHTTPResponse(MESSAGE.f.value)


@csrf_exempt
def GetDataForHeatMap(request):
	try:
		# data_type = request.GET.get('data-type')
		
		# get data points in <2 days
		now = datetime.now()
		two_days_ago = now - timedelta(days=2)
		points = Sample.objects.filter(time__range=(two_days_ago, now))

		result = []
		for p in points:
			point = {}
			point['longtitude'] = p.longtitude
			point['latitude'] = p.latitude
			point['moisture'] = p.moisture
			point['transpiration'] = p.transpiration
			result.append(point)

		# print('points count:', len(result))
		return HttpResponse(simplejson.dumps(result))
	
	except Exception as e:
		print('Exception GetDataForHeatMap', e)
		return generateHTTPResponse(MESSAGE.f.value)

############################################################

# calculate transpiration
def __Get_Transpiration(leaf_temp, air_temp, humidity):	
	# a0: Intercept of water stress line for tomatoes in sunlight (Temp[degC],Pressure[kPa])
	# a1: Slope of water stress line for tomatoes in sunlight (Temp[degC],Pressure[kPa])
	# t_svp: Temp range for empirical SVP(Saturated Vapor Pressure) relationship 
	# p_svp: Pressures for empirical SVP(Saturated Vapor Pressure) relationship [kPa]
	(a0, a1) = getWSLParameter()
	(t_svp, p_svp) = getSVPParameter()

	t_svp = np.array(t_svp)
	p_svp = np.array(p_svp)

	f_svp = interpolate.interp1d(t_svp, p_svp, kind='linear') # Linearly interpolate SVP relationship
	svp_a = f_svp(air_temp) # SVP for air temp
	vpd = (1-(humidity/100))*svp_a # VPD (Vapor Pressure Defecit)

	NWSB = lambda vpdx: a0 + a1*(vpdx) # NWSB (Non-Water Stressed Baseline)

	svp_leaf0 = f_svp(air_temp+a0) # SVP for leaf at theoretical 0 transpiration
	vpd_neg = svp_leaf0 - svp_a # distance to travel back on VPD axis to intersect with NWSB
	ws = a0 - a1 * vpd_neg # WS (Water Stress)

	cwsi = (ws-(leaf_temp-air_temp))/(ws-NWSB(vpd)) # CWSI (Crop Water Stress Index)

	return cwsi

'''
# generate moisture image
def __GenImg_Moisture():
	

# generate compaction image
def __GenImg_Compaction():


# generate transpiration image
def __GenImg_Transpiration():

'''







