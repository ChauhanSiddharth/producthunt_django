from django.contrib import admin
from accounts.models import UserProfile, FriendModel
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FriendModel)