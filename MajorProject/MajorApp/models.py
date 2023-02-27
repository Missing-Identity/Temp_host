from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

# Create your models here.
class UrlModel(models.Model):
    url = models.CharField(max_length=200)

class Result(models.Model):
    success = models.CharField(max_length=50)
    risk_score = models.CharField(max_length=50)
    phishing = models.CharField(max_length=50)
    category = models.CharField(max_length=200)
    malware = models.CharField(max_length=200)
    screenshot = models.CharField(max_length=500)