from django.contrib import admin
from reg.models import userInfo
class userAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(userInfo,userAdmin)