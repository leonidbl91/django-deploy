from django.db import models
from cook.models import Cook,Location
from djangoratings.fields import RatingField
from os import makedirs,path
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

	
class DishDay(models.Model):
	day =  models.CharField(max_length=40,null=False)
	def __unicode__(self):
		return self.day
class DishFoodType(models.Model):
	food_type =  models.CharField(max_length=40,null=False)
	def __unicode__(self):
		return self.food_type

class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=1 
        super(DayOfTheWeekField,self).__init__(*args, **kwargs)

class FoodCategory(models.Model):
	category = models.CharField(max_length=60)
	def __unicode__(self):
		return self.category
	
	
class Dish(models.Model):
	dish_name = models.CharField(max_length=40,null=False)
	special_options = models.CharField(max_length=100,null=False)
	description = models.TextField(null=True,blank=True)
	cook = models.ForeignKey(Cook,null=False)
	days= models.ManyToManyField(DishDay, related_name='dish+', through='Dish_DishDay_ManyToMany')
	food_types=models.ManyToManyField(DishFoodType, related_name='dish+', through='Dish_FoodType_ManyToMany')
	price = models.DecimalField(max_digits=5, decimal_places=2)
	rating = RatingField(range=5,allow_anonymous = True,use_cookies = True,can_change_vote = True) # 5 possible rating values, 1-5
	category = models.ForeignKey(FoodCategory,null=False)
	def __unicode__(self):
		return self.dish_name


def dishimage_file_name(instance, filename):
	
	cur_dish=Dish.objects.filter(id=instance.dish_id)
	cur_dish=cur_dish[0]
	cur_cook=cur_dish.cook.full_name
	ending=filename.split('.');
	ending=ending[1]
	
	#decide file name
	if instance.overrideFileName is not None:
		fname=instance.overrideFileName
	else:
		fname=filename
	
	#build directory path
	path= '/'.join(['dishes_content',unicode(cur_cook),unicode(instance.dish_id)])
	try:
		makedirs(path)
	except OSError:
		pass
	
	#concat filename
	imgPath='/'.join([path,fname])

	return unicode(imgPath)
	
def dishimage_Thumb_file_name(instance, filename):
	
	cur_dish=Dish.objects.filter(id=instance.dish_id)
	cur_dish=cur_dish[0]
	cur_cook=cur_dish.cook.full_name
	ending=filename.split('.');
	ending=ending[1]
	
	#decide file name
	if instance.overrideFileName is not None:
		fname=instance.overrideFileName
	else:
		fname=filename
	
	#build directory path
	path= '/'.join(['dishes_content',unicode(cur_cook),unicode(instance.dish_id),'_thumb'])
	try:
		makedirs(path)
	except OSError:
		pass
	
	#concat filename
	imgPath='/'.join([path,fname])

	return unicode(imgPath)

	
#may be several images for a single dish
class DishImage(models.Model):
	dish = models.ForeignKey(Dish, related_name='images')
	image = models.ImageField(upload_to=dishimage_file_name)
	thumbnail = models.ImageField( upload_to=dishimage_Thumb_file_name, blank=True, null=True)
	main =models.BooleanField(default=False)
	overrideFileName = None
	
	def save(self):
	
		# Save this photo instance first
		super(DishImage, self).save()
	
		# Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = (400, 400)

		fpath=dishimage_file_name(self,self.image.name)
		fpath='/'.join([settings.MEDIA_ROOT,fpath])
	
		
		# Open original photo which we want to thumbnail using PIL's Image object
		savedImage = Image.open(fpath)

		
		if savedImage.mode not in ('L', 'RGB'):
			savedImage = image.convert('RGB')

		savedImage.thumbnail(THUMBNAIL_SIZE,Image.ANTIALIAS)

		# Save the thumbnail
		temp_handle = StringIO()
		savedImage.save(temp_handle, 'png')  # image stored to stringIO

		temp_handle.seek(0)  # sets position of file to 0

		# Save to the thumbnail field
		suf = SimpleUploadedFile(path.split(self.image.name)[-1],
		temp_handle.read(), content_type='image/png')  # reads in the file to save it
		
		thpath=suf.name+'.png'
		self.thumbnail.save(thpath, suf, save=False)
		
		#Save this photo instance again to save the thumbnail
		super(DishImage, self).save()
	
	
	
	def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
		storage, path = self.image.storage, self.image.path
        # Delete the model before the file
		super(DishImage, self).delete(*args, **kwargs)
        # Delete the file after the model
		storage.delete(path)


class Dish_FoodType_ManyToMany(models.Model):
    dish = models.ForeignKey(Dish)
    food_type = models.ForeignKey(DishFoodType)

class Dish_DishDay_ManyToMany(models.Model):
    dish = models.ForeignKey(Dish)
    day = models.ForeignKey(DishDay)
	




