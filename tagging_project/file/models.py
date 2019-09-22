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
    score = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2)
    ymin = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2)
    xmin = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2)
    ymax = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2)
    xmax = models.DecimalField(blank=False, null=False, max_digits=5, decimal_places=2)
    area = models.DecimalField(blank=False, default=0, max_digits=5, decimal_places=2)
    class_name = models.CharField(max_length=100, blank=False, null=False)
    class_name_fa = models.CharField(max_length=100, default='')
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=False)
