from django.db import models

# Create your models here.

class Urls(models.Model):
    full_url = models.CharField(max_length=100)
    shortened_url = models.CharField(max_length=100, null=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return str(self.full_url + " - " + self.shortened_url)