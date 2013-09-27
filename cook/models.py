from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from os import makedirs,path
from djangoratings.fields import RatingField

class Location(models.Model):
	location = models.CharField(max_length=60)
	def __unicode__(self):
		return self.location

		
def cookimage_file_name(instance, filename):
	ending=filename.split('.');
	ending=ending[1]
	return ''.join(['cooks_images','/'+unicode(instance.user_id)+'.'+ending])

	
def cookimage_Thumb_file_name(instance, filename):

	#build directory path
	path= '/'.join(['cooks_images','_thumb'])
	try:
		makedirs(path)
	except OSError:
		pass
	
	ending=filename.split('.');
	ending=ending[1]
	#concat filename
	imgPath='/'.join([path,unicode(instance.user_id)+'.'+ending])

	return unicode(imgPath)


class Cook(models.Model):

	user = models.OneToOneField(User,null=False)
	full_name  = models.CharField(max_length=50,null=False) 
	facebook_link= models.URLField(blank=True, null=True)
	
	location = models.ForeignKey(Location,null=False)
	telephone = models.CharField(max_length=15,blank=True,null=True)
	address =  models.TextField(blank=True, null=True)
	about = models.TextField(null=True,blank=True)
	image = models.ImageField(upload_to=cookimage_file_name,)
	thumbnail = models.ImageField(upload_to=cookimage_Thumb_file_name, blank=True, null=True)
	
	speciality = models.TextField(null=True,blank=True)
	inspiration = models.TextField(null=True,blank=True)
	winner_dish = models.TextField(null=True,blank=True)
	
	cook_verified = models.BooleanField(default=False)
	supply_delivery = models.BooleanField(default=False)
	rating = RatingField(range=5,allow_anonymous = True,use_cookies = True,can_change_vote = True) # 5 possible rating values, 1-5
	#some statustic data
	
	def save(self):
		# Save this photo instance first
		super(Cook, self).save()
		
		# Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = (400, 400)
		
		fpath=cookimage_file_name(self,self.image.name)
		
		if not settings.MEDIA_ROOT=='':
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
		super(Cook, self).save()
	
	def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
		storage, path = self.image.storage, self.image.path
        # Delete the model before the file
		super(DishImage, self).delete(*args, **kwargs)
        # Delete the file after the model
		storage.delete(path)
	
	def __unicode__(self):
		return self.full_name
	




