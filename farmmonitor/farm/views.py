from django.shortcuts import render
from farm.models import *
from farm.forms import *
from django.views.decorators.csrf import csrf_exempt

from utils import *

@csrf_exempt
def NewSample(request):
	try:
		pos_x = float(request.POST.get('pos_x'))
		pos_y = float(request.POST.get('pos_y'))
		moisture = float(request.POST.get('moisture'))
		compaction = float(request.POST.get('compaction'))
		air_temp = float(request.POST.get('air_temp'))
		leave_temp = float(request.POST.get('leave_temp'))
		humidity = float(request.POST.get('humidity'))
		
		transpiration = __Get_Transpiration(leave_temp, air_temp, humidity)

		new_sample = Sample(pos_x=pos_x, pos_y=pos_y, moisture=moisture, compaction=compaction,
			air_temp=air_temp, leave_temp=leave_temp, humidity=humidity, transpiration=transpiration)
		new_sample.save()

		form = PhotoForm(request.POST, request.FILES)
		photo = None
		print('form is valid?')
		if form.is_valid():
			print('form is valid')
			photo = request.FILES['photo']

		new_sample.photo = photo
		new_sample.save()

		return generateHTTPResponse(MESSAGE.s.value)
	except Exception as e:
		print('Exception NewSample', e)
		return generateHTTPResponse(MESSAGE.f.value)


# @csrf_exempt
# def NewGrid(request):
# 	try:
# 		rows = int(request.POST.get('rows'))
# 		cols = int(request.POST.get('cols'))
# 		west = int(request.POST.get('west'))
# 		east = int(request.POST.get('east'))
# 		north = int(request.POST.get('north'))
# 		south = int(request.POST.get('south'))

# 		Grid.objects.all().delete()

# 		foot_x = (east-west) / cols
# 		foot_y = (north-south) / rows
# 		x = west
# 		y = south
		
# 		for i in range(0, rows):
# 			for j in range(0, cols):
# 				print('%d, %d' % (x, y))
# 				__Insert_Grid(x, x+foot_x, y, y+foot_y)
# 				y = y+foot_y
# 			x = x+foot_x
# 			y = south

# 		return generateHTTPResponse(MESSAGE.s.value)
# 	except Exception as e:
# 		print('Exception NewGrid', e)
# 		return generateHTTPResponse(MESSAGE.f.value)	


# @csrf_exempt
# def NewMoisture(request):
# 	try:
# 		moisture = float(request.POST.get('moisture'))
# 		pos_x = float(request.POST.get('pos_x'))
# 		pos_y = float(request.POST.get('pos_y'))

# 		grid = __Check_Grid(pos_x, pos_y)

# 		print('grid_id', grid.id)

# 		if grid is None:
# 			return generateHTTPResponse(MESSAGE.fg.value)

# 		new_moisture = Moisture(grid_id=grid, moisture=moisture)
# 		new_moisture.save()
# 		return generateHTTPResponse(MESSAGE.s.value)
# 	except Exception as e:
# 		print('Exception NewMoisture', e)
# 		return generateHTTPResponse(MESSAGE.fg.value)



############################################################

# calculate transpiration
def __Get_Transpiration(leave_temp, air_temp, humidity):	
	### transpiration algorithm:
	ans = leave_temp+air_temp+humidity

	return ans

'''
# generate moisture image
def __GenImg_Moisture():
	

# generate compaction image
def __GenImg_Compaction():


# generate transpiration image
def __GenImg_Transpiration():

'''

# def __Check_Grid(x, y):
# 	grid = Grid.objects.get(min_x__lte=x, min_y__lte=y, max_x__gt=x, max_y__gt=y)
# 	return grid


# def __Insert_Grid(min_x, max_x, min_y, max_y):
# 	new_grid = Grid(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)
# 	new_grid.save()








