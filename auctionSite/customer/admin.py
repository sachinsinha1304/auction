from django.contrib import admin
from .models import*

# Register your models here.

class AdminItem(admin.ModelAdmin):
    list_display= ["name","category",'user','initialPrice','closingDate','status']


class AdminUser(admin.ModelAdmin):
    list_display= ["name","contact",'gender','email']

class AdminBidd(admin.ModelAdmin):
    list_display= ["itemId","custId",'bidd']

class AdminSold(admin.ModelAdmin):
    list_display= ["itemId","custId",'price']


admin.site.register(item,AdminItem)
admin.site.register(userDetails,AdminUser)
admin.site.register(Biddings,AdminBidd)
admin.site.register(SoldItems,AdminSold)
admin.site.register(Category)
admin.site.register(Comments)
