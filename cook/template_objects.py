from django.db import models
from cook.models import Cook

class UserCredentials:
	def __init__(self,dict):
		self.user_dict={}
		self.user_dict.update(dict)

class CookCredentials:
	def __init__(self,dict):
		self.cook_dict={}
		self.cook_dict.update(dict)
		
class DishCredentials:
	def __init__(self,dict):
		self.dish_dict={}
		self.dish_dict.update(dict)