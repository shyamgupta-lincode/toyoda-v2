from django.contrib import admin
from accounts.models import User,User_Client,User_SI,Client,SI,User_Master,User_Admin,User_Business_Manager,User_Sales_Executive
from django.contrib.auth.admin import UserAdmin

admin.site.register(User)
admin.site.register(User_Master)
admin.site.register(User_Admin)
admin.site.register(User_Business_Manager)
admin.site.register(User_Sales_Executive)
admin.site.register(User_Client)
admin.site.register(User_SI)
admin.site.register(Client)
admin.site.register(SI)
