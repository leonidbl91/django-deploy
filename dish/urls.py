from django.conf.urls import patterns, include, url
from djangoratings.views import AddRatingFromModel


urlpatterns = patterns('',
	(r'^all_dishes/$','dish.views.all_dishes',{}),
	(r'^my_dishes/$','cook.views.my_dishes',{}),
	(r'^(?P<dish_id>\d+)/$','dish.views.dish',{}),
	(r'^edit_dish/(?P<dish_id>\d+)/$','cook.views.edit_dish',{}),
	url(r'rate-dish/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'dish',
        'model': 'dish',
        'field_name': 'rating',
    }),

)
