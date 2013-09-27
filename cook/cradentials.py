
from cook.models import Cook,Location
from dish.models import Dish,Dish_DishDay_ManyToMany,Dish_FoodType_ManyToMany,DishImage,DishDay,DishFoodType,FoodCategory
from django.conf import settings
from cook.template_objects import UserCredentials,CookCredentials,DishCredentials


#returns the cook that matches the request user
def get_cook_profile_data(request):
	if (request.user.is_authenticated()):
		cur_cook=Cook.objects.filter(user=request.user)
		if len(cur_cook)>0:
			cook=cur_cook[0]
		else:
			cook=None
	else:
		cook=None
	return cook
	
#returns the cook that matches the  user
def get_cook_from_user(user):
	cur_cook=Cook.objects.filter(user=user)
	if len(cur_cook)>0:
		cook=cur_cook[0]
	else:
		cook=None
	return cook

#returns the path to the image
def get_cook_profile_image(cook):
	#image=cook.image
	image=cook.thumbnail
	return '/'+'/'.join(['media',unicode(image)])

	
#returns credentials according to the logined cook
def get_cook_credentials(user):
	cook_model=get_cook_from_user(user)
	if cook_model is None:
		return;
	cook_dishes=Dish.objects.filter(cook=cook_model)
	all_categories=FoodCategory.objects.all()
	
	
	dish_cred_list=[]
	#all cook dishes credentials
	for dish in cook_dishes:
		#creating list of dish credentials
		dish_cred=get_dish_credentials(dish)
		dish_cred_list.append(dish_cred)
	
	#dishes by categories
	
	category_dict={}
	for cat in all_categories:
		cat_dishes=cook_dishes.filter(category=cat)
		
		
		cat_dish_cred_list=[]
		for dish in cat_dishes:
			#creating list of dish credentials
			cat_dish_cred=get_dish_credentials(dish)
			cat_dish_cred_list.append(cat_dish_cred)
		category_dict.update({cat:cat_dish_cred_list})
	
	if(len(dish_cred_list)>3):
		short_dish_cred_list=dish_cred_list[0:3]
	else:
		short_dish_cred_list=dish_cred_list
	

	profile_image=get_cook_profile_image(cook_model)
	cook_credentials=CookCredentials({'id':cook_model.id,'full_name':cook_model.full_name,'location':cook_model.location,'image':profile_image,
	'telephone':cook_model.telephone,'address':cook_model.address,'about':cook_model.about,'speciality':cook_model.speciality,
	'all_categories':all_categories,'category_dict':category_dict,'cook_verified':cook_model.cook_verified,'supply_delivery':cook_model.supply_delivery,
	'facebook_link':cook_model.facebook_link,
	'inspiration':cook_model.inspiration,'winner_dish':cook_model.winner_dish,'dish_cred_list':dish_cred_list,'short_dish_cred_list':short_dish_cred_list,'cook':cook_model,
	})
	return cook_credentials
	
	
#returns credentials according to the logined user
def get_user_credentials(user):
	cook_model=get_cook_from_user(user)
	if cook_model is None:
		return;
	profile_image=get_cook_profile_image(cook_model)
	user_credentials=UserCredentials({'image':profile_image,'name':unicode(user)})
	return user_credentials


#returns the path to the image
def get_mainImage_object(dish):
	mainImg=None
	img_list=dish.images.all()
	
	if len(img_list)>0:
		img_list=list(img_list)
		mainImg=img_list[0]
		
		for elem in img_list:
			if elem.main==True:
				return elem				

	return mainImg
	
#return path to dish image
def get_dish_img_path(DishImage):
	#path ='/'.join(['/media',str(DishImage.image)])
	path ='/'.join(['/media',str(DishImage.thumbnail)])
	return path
	
	
#returns all the data according the input dish
def get_dish_credentials(dish):
	mainImg=None
	images =[]

	img_list=dish.images.all()
	
	if len(img_list)>0:
		img_list=list(img_list)
	
		for elem in img_list:
			
			if elem.main == True and mainImg is None:
			
				mainImg=get_dish_img_path(elem) 
				images.insert(0,elem)
				continue;
			
			images.append(elem)
	
	url='/dish/'+unicode(dish.id)
	dish_id=unicode(dish.id)

	dish_credentials=DishCredentials({'dishName':dish.dish_name,'price':dish.price,
										'specialOp':dish.special_options,'desc':dish.description,
										'mainImage':mainImg,'url':url,'images':images,'id':dish_id,'dish':dish,'food_types':dish.food_types.all(),
										'days':dish.days.all(),
										})
	return dish_credentials

