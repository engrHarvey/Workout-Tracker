from django.contrib import admin
from .models import BMIRecord, UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)
