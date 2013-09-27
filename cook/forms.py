from django import forms
from django.forms import ModelForm
from cook.models import Cook,Location
from django.contrib.auth.models import User
from django.db import models

class CookEditForm(forms.Form):
	#cook params
	full_name=forms.CharField(label = (u'Full Name'),required=True)
	telephone = forms.CharField(max_length=15,required=False)
	address =  forms.CharField(required=False)
	about = forms.CharField(widget=forms.Textarea(attrs={'style': "width:90%;", 'rows': 10}),required=False )
	speciality = forms.CharField(widget=forms.Textarea(attrs={'style': "width:90%;", 'rows': 10}),required=False )	
	inspiration = forms.CharField(widget=forms.Textarea(attrs={'style': "width:90%;", 'rows': 10}),required=False )
	winner_dish = forms.CharField(widget=forms.Textarea(attrs={'style': "width:90%;", 'rows': 10}),required=False )
	facebook_link=forms.URLField(required=False)
	
	location = forms.ModelMultipleChoiceField(queryset=Location.objects.all())

	supply_delivery=forms.BooleanField(widget=forms.CheckboxInput,required=False)
	def clean_location(self):
		location=self.cleaned_data['location']
		if not len(location) == 1:
			raise forms.ValidationError("select only one location")
		else:
			return self.cleaned_data['location']
	def clean(self):
		return self.cleaned_data
		