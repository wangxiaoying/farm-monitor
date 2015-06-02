from django.shortcuts import render
from farm.models import *
from farm.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import time as single_time
import simplejson
import numpy as np
from datetime import datetime, timedelta, time
from scipy import interpolate
from matplotlib.mlab import griddata

from utils import *

@csrf_exempt
def NewSample(request):
	try:
		longtitude = float(request.POST.get('longtitude'))
		latitude = float(request.POST.get('latitude'))
		moisture = float(request.POST.get('moisture'))
		transpiration = float(request.POST.get('transpiration'))
		air_temp = float(request.POST.get('air_temp'))
		leaf_temp = float(request.POST.get('leaf_temp'))
		humidity = float(request.POST.get('humidity'))

		date_time = single_time.strptime(request.POST.get('datetime'), '%m.%d.%Y %H%M.%S')
		dt = datetime.fromtimestamp(single_time.mktime(date_time))

		# transpiration = __Get_Transpiration(leaf_temp, air_temp, humidity)

		new_sample = Sample(longtitude=longtitude, latitude=latitude, moisture=moisture,
			air_temp=air_temp, leaf_temp=leaf_temp, humidity=humidity, transpiration=transpiration, time=dt, 
			both=moisture-transpiration)
		new_sample.save()

		form = PhotoForm(request.POST, request.FILES)
		photo = None
		if form.is_valid():
			photo = request.FILES['photo']
			if photo is not None:
				new_sample.photo = photo
				new_sample.save()

		return generateHTTPResponse('NewSample', MESSAGE.s.value)
	except Exception as e:
		print('Exception NewSample', e)
		return generateHTTPResponse('NewSample', MESSAGE.f.value)


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
			
		return generateHTTPResponse('TestHttpConnection', MESSAGE.s.value)
	except Exception as e:
		print('Exception TestHttpConnection', e)
		return generateHTTPResponse('TestHttpConnection', MESSAGE.f.value)


@csrf_exempt
def GetDataPoints(request):
	try:
		# get data points in <2 days
		# now = datetime.now()
		# two_days_ago = now - timedelta(days=2)
		
		result = __Get_Data(now=True)

		return HttpResponse(simplejson.dumps(result))
	
	except Exception as e:
		print('Exception GetDataPoints', e)
		return generateHTTPResponse('GetDataPoints', MESSAGE.f.value)

@csrf_exempt
def GetHistoryData(request):
	try:
		time_from = request.GET.get('time_from')
		time_to = request.GET.get('time_to')

		result = __Get_Data(time_from=time_from, time_to=time_to)

		return HttpResponse(simplejson.dumps(result))

	except Exception as e:
		print('Exception GetHistoryData', e)
		return generateHTTPResponse('GetHistoryData', MESSAGE.f.value)

@csrf_exempt
def GetPointDetail(request):
	try:
		pid = request.GET.get('id')
		point = Sample.objects.get(id=pid)

		result = {}
		result['id'] = point.id
		result['longtitude'] = point.longtitude
		result['latitude'] = point.latitude
		result['moisture'] = point.moisture
		result['air_temp'] = point.air_temp
		result['leaf_temp'] = point.leaf_temp
		result['humidity'] = point.humidity
		result['transpiration'] = point.transpiration
		result['time'] = point.time.strftime(getDatetimeFormat())
		if point.photo:
			result['photo'] = point.photo.url	

		return HttpResponse(simplejson.dumps(result))

	except Exception as e:
		print('Exception GetPointDetail', e)
		return generateHTTPResponse('GetPointDetail', MESSAGE.f.value)


@csrf_exempt
def GetImportantData(request):
	try:
		now = datetime.now()
		two_days_ago = now - timedelta(days=2)
		points = Sample.objects.filter(time__range=(two_days_ago, now)).filter(Q(transpiration__lt=getImpoDataMax('transpiration'))|
			Q(transpiration__gt=getImpoDataMin('transpiration'))|Q(moisture__lt=getImpoDataMax('moisture'))|Q(moisture__gt=getImpoDataMin('moisture')))

		result = []
		for p in points:
			point = {}
			point['id'] = p.id
			point['longtitude'] = p.longtitude
			point['latitude'] = p.latitude
			point['moisture'] = p.moisture
			point['transpiration'] = p.transpiration
			result.append(point)

		# print('points count:', len(result))
		return HttpResponse(simplejson.dumps(result))

	except Exception as e:
		print('Exception GetImportantData', e)
		return generateHTTPResponse('GetImportantData', MESSAGE.f.value)


@csrf_exempt
def GetHeatMap(request):
	try:
		hm_type = request.GET.get('type')
		points = __Get_Points()
		x = []
		y = []
		z = []
		for p in points:
			x.append(float(p.latitude)+getShiftValue('latitude'))
			y.append(float(p.longtitude)+getShiftValue('longtitude'))
			z.append(float(getattr(p, hm_type)))

		print('GetHeatMap', x)
		print('GetHeatMap', y)

		result = __Do_Seperate_Interpolate(x, y, z)
		return HttpResponse(simplejson.dumps(result))
	except Exception as e:
		print('Exception GetHeatMap', e)
		return generateHTTPResponse('GetHeatMap', MESSAGE.f.value)

@csrf_exempt
def DeleteFakePoints(request):
	try:
		last_id = request.GET.get('id')
		Sample.objects.filter(id__gt=last_id).delete()

		return generateHTTPResponse('DeleteFakePoint', MESSAGE.s.value)
	except Exception as e:
		print('Exception DeleteFakePoint', e)
		return generateHTTPResponse('DeleteFakePoint', MESSAGE.f.value)

def ResetPointPosition(request):
	try:
		last_id = request.GET.get('id')

		points = Sample.objects.filter(id__gt=last_id)
		for p in points:
			p.latitude = p.latitude+getShiftValue('latitude')
			p.longtitude = p.longtitude+getShiftValue('longtitude')

		return generateHTTPResponse('ResetPointPosition', MESSAGE.s.value)
	except Exception as e:
		print('ResetPointPosition', e)
		return generateHTTPResponse('ResetPointPosition', MESSAGE.f.value)

############################################################

def __Get_Points(time_from=(datetime.now() - timedelta(days=2)), time_to=datetime.now()):
	try:
		points = Sample.objects.filter(Q(time__gte=time_from), Q(time__lte=time_to))
		if 0 == len(points):
			nrst_point = Sample.objects.latest('time')
			# print(type(nrst_point), nrst_point)
			nrst_day = nrst_point.time.date()
			print('nrst_day in string', str(nrst_day))
			# print(type(nrst_day), nrst_day)
			# points = Sample.objects.filter(time__contains=str(nrst_day))
			# points = Sample.objects.filter(time__year=nrst_day.year, time__month=nrst_day.month, time__day=nrst_day.day)
			points = Sample.objects.filter(time__range=(datetime.combine(nrst_day, time.min), datetime.combine(nrst_day, time.max)))
			# print(len(points))

		return points
	except Exception as e:
		print('Exception __Get_Points', e)

def __Get_Data(time_from=(datetime.now() - timedelta(days=2)), time_to=datetime.now(), now=False):
	try:
		print(time_from, time_to)
		points = __Get_Points(time_from, time_to)
		print(len(points))
		
		result = {}
	
		# if now:
		# 	x = []
		# 	y = []
		# 	zm = []
		# 	zt = []
		# 	for p in points:
		# 		x.append(float(p.latitude))
		# 		y.append(float(p.longtitude))
		# 		zm.append(float(p.moisture))
		# 		zt.append(float(p.transpiration))
		# 	result.update(__Do_Interpolate(x, y, zm, zt))
	
		data = []
		for p in points:
			point = {}
			point['id'] = p.id
			point['longtitude'] = float(p.longtitude)+getShiftValue('longtitude')
			point['latitude'] = float(p.latitude)+getShiftValue('latitude')
			point['moisture'] = p.moisture
			point['air_temp'] = p.air_temp
			point['leaf_temp'] = p.leaf_temp
			point['humidity'] = p.humidity
			point['transpiration'] = p.transpiration
			point['time'] = p.time.strftime(getDatetimeFormat())
			if p.photo:
				point['photo'] = p.photo.url
			data.append(point)
	
		result['data'] = data
	
		return result
	except Exception as e:
		print('__Get_Data', e)


def __Do_Interpolate(x, y, zm, zt):
	try:
		xi = np.linspace(min(x), max(x), getWidthPixelNum())
		step_size = (max(x)-min(x))/getWidthPixelNum()
		yi = np.arange(min(y), max(y), step_size)
	
		zmi = griddata(x, y, zm, xi, yi, interp='linear').tolist()
		zti = griddata(x, y, zt, xi, yi, interp='linear').tolist()
	
		result = {}

		result['min-x'] = min(x)
		result['min-y'] = min(y)
		result['max-x'] = max(x)
		result['max-y'] = max(y)
		result['max-m'] = max(zm)
		result['min-m'] = min(zm)
		result['max-t'] = max(zt)
		result['min-t'] = min(zt)
		result['all-moist'] = zmi
		result['all-trans'] = zti
	
		return result
	except Exception as e:
		print('__Do_Interpolate', e)


def __Do_Seperate_Interpolate(x, y, z):
	try:
		xi = np.linspace(min(x), max(x), getWidthPixelNum())
		step_size = (max(x)-min(x))/getWidthPixelNum()
		yi = np.arange(min(y), max(y), step_size)
	
		zi = griddata(x, y, z, xi, yi, interp='linear').tolist()
		
		print('__Do_Interpolate', x)
		print('__Do_Interpolate', y)
		print(min(x), min(y), max(x), max(y))

		result = {}
		result['min-x'] = min(x)
		result['min-y'] = min(y)
		result['max-x'] = max(x)
		result['max-y'] = max(y)
		result['max-z'] = max(z)
		result['min-z'] = min(z)
		result['all-image'] = zi
	
		return result
	except Exception as e:
		print('__Do_Seperate_Interpolate', e)


# calculate transpiration
def __Get_Transpiration(leaf_temp, air_temp, humidity):	
	try:
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
	except Exception as e:
		print('__Get_Transpiration', e)



'''
# generate moisture image
def __GenImg_Moisture():
	

# generate compaction image
def __GenImg_Compaction():


# generate transpiration image
def __GenImg_Transpiration():

'''







