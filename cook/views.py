from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http  import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from cook.models import Cook,Location
from dish.models import Dish,Dish_DishDay_ManyToMany,Dish_FoodType_ManyToMany,DishImage,DishDay,DishFoodType
from django.conf import settings
from dish.forms import dishEditForm
from cook.forms import CookEditForm
from cook.cradentials import get_cook_profile_data,get_user_credentials,get_cook_credentials,get_cook_from_user,get_mainImage_object,get_dish_img_path,get_dish_credentials
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

	
def all_cooks(request):
	
	all_locations=Location.objects.all()
	all_types=DishFoodType.objects.all()
	filter=buildFilterFromQuery(request)
	page = request.GET.get('page')
	all_credentials=[]
	
	#filtering all_cooks
	if filter.loc  is not None:
		locations=Location.objects.filter(location=filter.loc)
		cooks=Cook.objects.filter(location__in=locations)
		all_cooks=cooks
	elif filter.type:
		selected_types=DishFoodType.objects.filter(food_type=filter.type)
		all_dishes=Dish.objects.filter(food_types__in=selected_types)
		cooks=[]
		for dish in all_dishes:
			if not dish.cook in cooks:
				cooks.append(dish.cook)
		all_cooks=cooks
	else:
		all_cooks=Cook.objects.all()
			
	
	for cook in all_cooks:
		cook_cred=get_cook_credentials(cook.user)
		all_credentials.append(cook_cred)
	
	paginator=Paginator(all_cooks,5)	
	try:
		all_cooks = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		all_cooks = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		all_cooks = paginator.page(paginator.num_pages)
	

	if request.user.is_authenticated():
		credentials=get_user_credentials(request.user)
		return render_to_response('all_cooks.html',
		{'all_cooks_credentials':all_credentials,'user_credentials':credentials,'dishes':all_cooks,'all_locations':all_locations,'all_types':all_types,},
		context_instance= RequestContext(request))
	else:
		return render_to_response('all_cooks.html',
		{'all_cooks_credentials':all_credentials,'dishes':all_cooks,'all_locations':all_locations,'all_types':all_types,},
		context_instance= RequestContext(request))
	
#for all cooks filter	
class qfilter:
	loc=None
	price1=None
	price2=None
	type=None
def buildFilterFromQuery(request):
 
	filter= qfilter()

	if 'qp' in request.GET and request.GET['qp']:
		filter.loc = request.GET['qp']
	if 'qt' in request.GET and request.GET['qt']:
		price = request.GET['qt'].split(',')
		filter.price1=price[0]
		filter.price2=price[1]
		
	if 'qd' in request.GET and request.GET['qd']:
		filter.type=request.GET['qd']
	return filter;

def cook(request,cook_id):
	cur_cook=get_object_or_404(Cook,id=cook_id)
	#trying to view its own profile
	if cur_cook.user == request.user:
		return HttpResponseRedirect('/cook/profile')
	
	cook_credentials =get_cook_credentials(cur_cook.user)
	
	if request.user.is_authenticated():
		credentials=get_user_credentials(request.user)
		return render_to_response('cook.html',
		{'cook':cur_cook,'user_credentials':credentials,'cook_credentials':cook_credentials,},
		context_instance= RequestContext(request))
	else:
		return render_to_response('cook.html',
		{'cook':cur_cook,'cook_credentials':cook_credentials,},
		context_instance= RequestContext(request))
		
		

@login_required(login_url='/login/')
def edit_cook(request):
	cur_cook=get_cook_from_user(request.user)
	credentials=get_user_credentials(request.user)
	cook_credentials=get_cook_credentials(request.user)
	if request.method=='POST':
			form=CookEditForm(request.POST,request.FILES)
			
			if form.is_valid():
				test="None"
				
			#try:						
				#cook creation
				cur_cook.full_name=form.cleaned_data['full_name']
				cur_cook.telephone=form.cleaned_data['telephone']
				cur_cook.address=form.cleaned_data['address']
				cur_cook.about=form.cleaned_data['about']
				cur_cook.speciality=form.cleaned_data['speciality']
				cur_cook.inspiration=form.cleaned_data['inspiration']
				cur_cook.winner_dish=form.cleaned_data['winner_dish']
				cur_cook.facebook_link=form.cleaned_data['facebook_link']
				cur_cook.supply_delivery=form.cleaned_data['supply_delivery']
				location=form.cleaned_data['location']
				cur_cook.location=location[0]
				
				#if we need to change profile image
				if len(request.FILES)>0:
					try:
						cur_cook.image.delete()			
					except:
						pass
					cur_cook.image=request.FILES['profImg']
				
				cur_cook.save()
				return HttpResponseRedirect('/cook/profile')
			#except:	
				#user already exist or other error

				return render_to_response('edit_cook.html',
					{'user_credentials':credentials,'form':form,'cook_credentials':cook_credentials,},
					context_instance= RequestContext(request))
			else:

				return render_to_response('edit_cook.html',
						{'user_credentials':credentials,'form':form,'cook_credentials':cook_credentials,},
						context_instance= RequestContext(request))
	else:
		a=cur_cook.speciality
		b=cur_cook.winner_dish
	
		"""user is not submiting the form.show blank registration"""
		form= CookEditForm(initial={'full_name': cur_cook.full_name,
									'telephone':cur_cook.telephone,'address':cur_cook.address,
									'about':cur_cook.about,'speciality':cur_cook.speciality,
									'inspiration':cur_cook.inspiration,'winner_dish':cur_cook.winner_dish,'location':Location.objects.filter(location=cur_cook.location),
									'supply_delivery':cur_cook.supply_delivery,'facebook_link':cur_cook.facebook_link,
									}) 
		return render_to_response('edit_cook.html',{'user_credentials':credentials,'form':form,'cook_credentials':cook_credentials,},context_instance=RequestContext(request))
	
	
def main_view(request):
	cur_cook=get_cook_profile_data(request)
	all_dishes=Dish.objects.all()
	for dish in all_dishes:
		mainImg=get_mainImage_object(dish)
		if mainImg is not None:
			dish.mainImage=get_dish_img_path(mainImg)	
		else:
			dish.mainImage=None
	
	all_locations=Location.objects.all()
		
	if request.user.is_authenticated():
		credentials=get_user_credentials(request.user)
		return render_to_response('main.html',
		{'authenticated':True,'dishes':all_dishes,'user_credentials':credentials,'name' :request.user,'all_locations':all_locations,},
		context_instance= RequestContext(request))
	else:
		return render_to_response('main.html',
		{'authenticated':False,'dishes':all_dishes,'all_locations':all_locations,},
		context_instance= RequestContext(request))

		
@login_required(login_url='/login/')		
def profile(request):
	cur_cook=get_cook_from_user(request.user)
	user_credentials=get_user_credentials(request.user)
	if cur_cook is None:
		#the user is not a cook
		return HttpResponseRedirect('/')
		
	else:
		
		cook_credentials=get_cook_credentials(request.user)
		
	dict={'user_credentials':user_credentials,'cook_credentials':cook_credentials,}
	
	return render_to_response('profile.html',dict,context_instance= RequestContext(request))
		
		

		
@login_required(login_url='/login/')			
def my_dishes(request):
	all_dishes=Dish.objects.filter(cook=request.user)
	for dish in all_dishes:
		if len(dish.images.all())>0:
			img_list=list(dish.images.all())
			dish.image=''.join([settings.SITE_URL,'media/',str(img_list[0].image)])
			
		else:
			dish.image=None
	credentials=get_user_credentials(request.user)
	return render_to_response('my_dishes.html',
	{'dishes':all_dishes,'user_credentials':credentials,},
	context_instance= RequestContext(request))
	
		
@login_required(login_url='/login/')	
def add_dish(request):

	cur_cook=get_cook_from_user(request.user)
	cook_credentials=get_cook_credentials(request.user)

	if request.method=='POST':
	
		form=dishEditForm(request.POST,request.FILES)
		if form.is_valid():
			nd=Dish()
			nd.cook=cur_cook
			
			#form inputs
			nd.dish_name=form.cleaned_data['dishName']
			nd.special_options = form.cleaned_data['specialOp']
			nd.description= form.cleaned_data['desc']
			nd.price= form.cleaned_data['price']
			nd.category=form.cleaned_data['category']
			nd.save()
		
			#set many to many fields
			days=form.cleaned_data['days']		
			for d in days:
				a= Dish_DishDay_ManyToMany()
				a.dish=nd
				a.day=d
				a.save()
	
			ftypes=form.cleaned_data['food_types']
			for t in ftypes:
				a= Dish_FoodType_ManyToMany()
				a.dish=nd
				a.food_type=t
				a.save()
			
			#uploading file
			for key, file in request.FILES.items():
				img=DishImage()
				if key=="img1": 
					img.main=True
				img.dish=nd
				img.image=file
				img.overrideFileName=key+file.name[-4:]
				img.save()
				
			return HttpResponseRedirect('/cook/profile')
		#form invalid
		else:
			return render_to_response('add_dish.html',{'form':form,'cook_cred':cook_credentials,},
			context_instance=RequestContext(request))
	
	#get reques
	else:
		form= dishEditForm() 
		return render_to_response('add_dish.html',{'form':form,'cook_cred':cook_credentials,},
		context_instance=RequestContext(request))
		
		
		

@login_required(login_url='/login/')	
def edit_dish(request,dish_id):
	credentials=get_user_credentials(request.user)
	cur_dish=get_object_or_404(Dish,id=dish_id)
	dish_cred=get_dish_credentials(cur_dish)

	cur_cook=get_cook_from_user(request.user)
	cook_credentials=get_cook_credentials(request.user)


	if request.method=='POST':
	
		form=dishEditForm(request.POST,request.FILES)
		
		if form.is_valid():
			
			nd=cur_dish

			#form inputs
			nd.dish_name=form.cleaned_data['dishName']
			nd.special_options = form.cleaned_data['specialOp']
			nd.description= form.cleaned_data['desc']
			nd.price= form.cleaned_data['price']		
			nd.save()
			
			#first remove old values days and types
			Dish_DishDay_ManyToMany.objects.filter(dish=cur_dish).delete()
			Dish_FoodType_ManyToMany.objects.filter(dish=cur_dish).delete()

			#set days and types
			days=form.cleaned_data['days']		
			for d in days:
				a= Dish_DishDay_ManyToMany()
				a.dish=nd
				a.day=d
				a.save()
	
			ftypes=form.cleaned_data['food_types']
			for t in ftypes:
				a= Dish_FoodType_ManyToMany()
				a.dish=nd
				a.food_type=t
				a.save()
			
			imgs=dish_cred.dish_dict['images']
			oldPath=None
			
			
			#uploading file and delete old file
			for key, file in request.FILES.items():		
				newImg=DishImage()
				if key=="img1": 
					idx=1 
					oldPath=dish_cred.dish_dict['mainImage']
					newImg.main=True

				elif key=="img2":
					idx=2;
					if len(imgs)>=2:
						oldPath=imgs[1].image.url	
				elif key=="img3":
					idx=3;
					if len(imgs)>=3:
						oldPath=imgs[2].image.url		
				elif key=="img4":
					idx=4;
					if len(imgs)>=4:
						oldPath=imgs[3].image.url		
				
				#get all dish images

				for img in imgs:
					p=img.image.url
					if oldPath is not None and oldPath in p:
						img.delete()
							

				newImg.dish=nd
				newImg.image=file
				newImg.overrideFileName=key+file.name[-4:]
				newImg.save()
				
			return HttpResponseRedirect('/cook/profile')
		
		#form invalid
		else:
			return render_to_response('edit_dish.html',{'form':form,'cook_cred':cook_credentials,'dish_cred':dish_cred,},
			context_instance=RequestContext(request))
	
	#get reques
	else:	
		form= dishEditForm(initial={'dishName': cur_dish.dish_name,
									'desc':cur_dish.description,'price':cur_dish.price,
									'specialOp':cur_dish.special_options,
									'days':dish_cred.dish_dict['days'],'food_types':dish_cred.dish_dict['food_types'],
									}) 
		return render_to_response('edit_dish.html',{'form':form,'cook_cred':cook_credentials,'dish_cred':dish_cred,'user_credentials':credentials,},
		context_instance=RequestContext(request))

