from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http  import HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from cook.models import Cook,Location
from dish.models import Dish,Dish_DishDay_ManyToMany,Dish_FoodType_ManyToMany,DishFoodType,FoodCategory
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cook.cradentials import get_cook_profile_data,get_user_credentials,get_cook_credentials,get_mainImage_object,get_dish_credentials


#dish main page
def dish(request,dish_id):
	cur_dish=get_object_or_404(Dish,id=dish_id)

	dish_credentials=get_dish_credentials(cur_dish)
	cook_credentials =get_cook_credentials(cur_dish.cook.user)
	
	if request.user.is_authenticated():
		credentials=get_user_credentials(request.user)
		return render_to_response('dish.html',
		{'dish_cred':dish_credentials,'user_credentials':credentials,'cook_cred':cook_credentials,},
		context_instance= RequestContext(request))
	else:
		return render_to_response('dish.html',
		{'dish_cred':dish_credentials,'cook_cred':cook_credentials},
		context_instance= RequestContext(request))
	

	#for all dishes filter	
class qfilter:
	loc=None
	price1=None
	price2=None
	type=None
	category= None
		
		
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
	if 'qc' in request.GET and request.GET['qc']:
		filter.category=request.GET['qc']
	return filter;
		

		#all dishes page
def all_dishes(request):

	
	page = request.GET.get('page')
	curl=request.path
	qstring=request.get_full_path()
	filter=buildFilterFromQuery(request)

	all_locations=Location.objects.all()
	all_categories=FoodCategory.objects.all()
	all_types=DishFoodType.objects.all()
	if filter.loc  is not None:
		locations=Location.objects.filter(location=filter.loc)
		cooks=Cook.objects.filter(location__in=locations)
		all_dishes=Dish.objects.filter(cook__in=cooks)

	elif  filter.price1:
		all_dishes=Dish.objects.filter(price__gte=filter.price1,price__lte=filter.price2)
	elif filter.type:
		selected_types=DishFoodType.objects.filter(food_type=filter.type)
		all_dishes=Dish.objects.filter(food_types__in=selected_types)
	elif filter.category:
		selected_categories=FoodCategory.objects.filter(category=filter.category)
		all_dishes=Dish.objects.filter(category__in=selected_categories)
	else :
		all_dishes=Dish.objects.all()
		
	paginator=Paginator(all_dishes,12)
	
	try:
		filteredDishes = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		filteredDishes = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		filteredDishes = paginator.page(paginator.num_pages)

	for dish in filteredDishes:
		mainImg=get_mainImage_object(dish)
		if mainImg is not None:
			dish.mainImage=''.join([settings.SITE_URL,'media/',str(mainImg.thumbnail)])				
		else:
			dish.mainImage=None
			
	if request.user.is_authenticated():
		credentials=get_user_credentials(request.user)
		return render_to_response('all_dishes.html',
		{'dishes':filteredDishes,'user_credentials':credentials,'qstring':qstring,'curl':curl,'all_locations':all_locations,
		'all_types':all_types,'all_categories':all_categories,},
		context_instance= RequestContext(request))
	else:
		return render_to_response('all_dishes.html',
		{'dishes':filteredDishes,'qstring':qstring,'curl':curl,'all_locations':all_locations,'all_types':all_types,'all_categories':all_categories,},
		context_instance= RequestContext(request))
	
	
