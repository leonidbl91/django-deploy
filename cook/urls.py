from django.conf.urls import patterns, include, url
from djangoratings.views import AddRatingFromModel

urlpatterns = patterns('',
	(r'^all_cooks/$','cook.views.all_cooks',{}),
	(r'^(?P<cook_id>\d+)/$','cook.views.cook',{}),
	(r'^add_dish/$','cook.views.add_dish'),
	(r'^profile/$','cook.views.profile'),
	(r'^edit_cook/$','cook.views.edit_cook'),
	url(r'rate-cook/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
        'app_label': 'cook',
        'model': 'cook',
        'field_name': 'rating',
    }),

)
