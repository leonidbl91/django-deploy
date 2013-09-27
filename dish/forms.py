from django import forms
from django.forms import ModelForm
from dish.models import Dish,DishDay,DishFoodType,DishImage,FoodCategory

class dishEditForm(forms.Form):
	dishName=forms.CharField(label = (u'שם המנה'),required=True)
	desc =  forms.CharField(label = (u'תיאור המנה'),widget=forms.Textarea,required=False)
	price = forms.CharField(label = (u'מחיר המנה'),required=True)
	specialOp = forms.CharField(label = (u'תוספות מיוחדות'),widget=forms.Textarea,required=False)
	days = forms.ModelMultipleChoiceField(label = (u'ימי הכנה'),queryset=DishDay.objects.all(),required=False)
	food_types = forms.ModelMultipleChoiceField(label = (u'סוג האוכל'),queryset=DishFoodType.objects.all(),required=False)
	category = forms.ModelChoiceField(queryset=FoodCategory.objects.all(),required=True)
	
	
	def clean(self):
		return self.cleaned_data
	