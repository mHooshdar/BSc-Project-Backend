from django.contrib import admin
from tagging_project.file.models import File, Category


# Register your models here.
class FileAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'file', 'result', 'description', 'description_fa', 'user']


class CategoryAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'class_id', 'score', 'xmin', 'xmax', 'ymin', 'ymax', 'area', 'class_name', 'class_name_fa', 'file']


admin.site.register(File, FileAdmin)
admin.site.register(Category, CategoryAdmin)
