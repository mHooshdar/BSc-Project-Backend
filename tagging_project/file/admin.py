from django.contrib import admin
from tagging_project.file.models import File
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class FileAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'file', 'description', 'user']


admin.site.register(File, FileAdmin)
