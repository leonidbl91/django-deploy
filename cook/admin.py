from django.contrib import admin
from cook.models import Cook,Location
from dish.models import DishImage,Dish,DishDay,DishFoodType,Dish_DishDay_ManyToMany,Dish_FoodType_ManyToMany,FoodCategory

admin.site.register(Cook)
admin.site.register(Location)
admin.site.register(FoodCategory)

class DishImageInline(admin.TabularInline):
    model = DishImage
    extra = 3
class DishDaysInline(admin.TabularInline):
	model=Dish_DishDay_ManyToMany
	
class DishFoodTypeInline(admin.TabularInline):
	model=Dish_FoodType_ManyToMany
	

class DishAdmin(admin.ModelAdmin):
    inlines = [ DishImageInline,DishDaysInline,DishFoodTypeInline ]
	
admin.site.register(Dish,DishAdmin)

admin.site.register(DishDay)
admin.site.register(DishFoodType)