from django.db import models
from django.contrib.auth import models as auth_models


# Create your models here.
class File(models.Model):
    file = models.ImageField(blank=False, null=False)
    result = models.ImageField(blank=True, null=False, upload_to='result')
    description = models.CharField(max_length=100, blank=True)
    description_fa = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE, null=False)


class Category(models.Model):
    class_id = models.IntegerField(blank=False, null=False)
    score = models.FloatField(blank=False, null=False)
    ymin = models.FloatField(blank=False, null=False)
    xmin = models.FloatField(blank=False, null=False)
    ymax = models.FloatField(blank=False, null=False)
    xmax = models.FloatField(blank=False, null=False)
    area = models.FloatField(blank=False, default=0)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    class_name_fa = models.CharField(max_length=100, default='')
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=False)
