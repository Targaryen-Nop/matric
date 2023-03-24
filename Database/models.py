from django.db import models

# Create your models here.
class Member(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=20)
    security = models.PositiveIntegerField()
    performance = models.PositiveIntegerField()

class Metricmodel(models.Model):
    logger  = models.PositiveIntegerField()
    vms = models.PositiveIntegerField()


