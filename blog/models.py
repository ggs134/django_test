from django.db import models
from django.utils import timezone
import keyUtils


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Info(models.Model):
    text = models.TextField()

class BitcoinAddress(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=500, default="test address")
    priv_key = models.CharField(max_length=500, default="test private key")
    priv_wif = models.CharField(max_length=500, default="test wif private key")