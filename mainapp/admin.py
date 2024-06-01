from django.contrib import admin

import mainapp.models


# Register your models here.
@admin.register(mainapp.models.Userdata)
class UserdataAdmin(admin.ModelAdmin):
    list_display = ['username', 'saved_results']
