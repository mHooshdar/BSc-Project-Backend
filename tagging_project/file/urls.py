from django.urls import path
from .views import *


urlpatterns = [
    path('', create_file),
    path('user/<int:user_id>', get_user_files),
    path('<int:file_id>', delete_file),
]