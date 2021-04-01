from django.contrib import admin
from accounts.models import User,User_Client,User_SI,Client,SI,User_Master
from django.contrib.auth.admin import UserAdmin

admin.site.register(User)
admin.site.register(User_Master)
admin.site.register(User_Client)
admin.site.register(User_SI)
admin.site.register(Client)
admin.site.register(SI)
