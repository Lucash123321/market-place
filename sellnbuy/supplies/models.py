from django.db import models
from django.contrib.auth.models import User


class Supply(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=20)
    picture = models.ImageField(upload_to="supply/", null=True, blank=True)
    desc = models.TextField()


