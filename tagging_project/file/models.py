from django.db import models
from django.contrib.auth import models as auth_models


# Create your models here.
class File(models.Model):
    file = models.ImageField(blank=False, null=False)
    description = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, null=True)
