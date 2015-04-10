from django.db import models
from utils import *

class Sample(models.Model):
	def photo_file(self, filename):
		url = 'photos/%s/%d-%s' % (self.time.date(), self.id, filename)
		return url

	pos_x = models.DecimalField(max_digits=5, decimal_places=2)
	pos_y = models.DecimalField(max_digits=5, decimal_places=2)
	moisture = models.DecimalField(max_digits=5, decimal_places=2)
	compaction = models.DecimalField(max_digits=5, decimal_places=2)
	air_temp = models.DecimalField(max_digits=4, decimal_places=2)
	leave_temp = models.DecimalField(max_digits=4, decimal_places=2)
	humidity = models.DecimalField(max_digits=5, decimal_places=2)
	transpiration = models.DecimalField(max_digits=5, decimal_places=2)
	photo = models.FileField(upload_to=photo_file)
	time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'id: %d | pos: %.2f-%.2f' % (self.id, self.pos_x, self.pos_y)


class NetworkTest(models.Model):
	def photo_file(self, filename):
		url = 'photos/test/%s' % (filename)
		return url
	message = models.DecimalField(max_digits=4, decimal_places=2)
	photo = models.FileField(upload_to=photo_file)

# class Image(models.Model):
# 	img_type = models.CharField(max_length=1, choices=IMAGECHOICE)
# 	image = models.FileField(upload_to='image_file')
# 	time = models.DateTimeField(auto_now_add=True)

# 	def __unicode__(self):
# 		return 'id: %d | type: %c' % (self.id, self.img_type)

# class Grid(models.Model):
# 	min_x = models.DecimalField(max_digits=5, decimal_places=2)
# 	max_x = models.DecimalField(max_digits=5, decimal_places=2)
# 	min_y = models.DecimalField(max_digits=5, decimal_places=2)
# 	max_y = models.DecimalField(max_digits=5, decimal_places=2)

# 	def __unicode__(self):
# 		return 'id: %d | x: %.2f~%.2f y: %.2f~%.2f' % (self.id, self.min_x, self.max_x, self.min_y, self.max_y)

# class Moisture(models.Model):
# 	grid_id = models.ForeignKey(Grid, related_name='grid_id_m')
# 	moisture = models.DecimalField(max_digits=5, decimal_places=2)
# 	time = models.DateTimeField(auto_now_add=True)

# 	def __unicode__(self):
# 		return 'id: %d | moist: %.2f' % (self.id, self.moisture)


# class Transpiration(models.Model):
# 	grid_id = models.ForeignKey(Grid, related_name='grid_id_t')
# 	transpiration = models.DecimalField(max_digits=5, decimal_places=2)
# 	time = models.DateTimeField(auto_now_add=True)

# 	def __unicode__(self):
# 		return 'id: %d | trans: %.2f' % (self.id, self.transpiration)