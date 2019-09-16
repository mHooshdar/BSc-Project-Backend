from django.urls import path
from .views import *


urlpatterns = [
    path('create', create_file),
    path('user/<int:user_id>', get_user_files)
]