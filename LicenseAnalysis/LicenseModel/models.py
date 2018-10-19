from django.db import models

# Create your models here.

class license_description(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=10)
    content = models.TextField()
