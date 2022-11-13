from django.contrib import admin
from accounts.models import CustomUser, FollowerFollowing


admin.site.register(CustomUser)
admin.site.register(FollowerFollowing)
