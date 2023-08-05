from django.db import models
from django.contrib.auth.models import User


class Supply(models.Model):
    user = models.ForeignKey(User, related_name="seller", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    desc = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='supplies/', blank=True, null=True)


class Comment(models.Model):
    rating_value = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    user = models.ForeignKey(User, related_name="comment_author", on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=rating_value)
    supply = models.ForeignKey(Supply, related_name="post_to_comment", on_delete=models.CASCADE)
    text = models.TextField()


class Message(models.Model):
    user = models.ForeignKey(User, related_name="message_author", on_delete=models.CASCADE)
    to = models.ForeignKey(User, related_name="message_receiver", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

