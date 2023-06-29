from django.db import models


class Supply(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=20)
    picture = models.ImageField(upload_to="supply/", null=True, blank=True)
    desc = models.TextField()


