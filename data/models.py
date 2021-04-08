from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Data(models.Model):
    name = models.CharField(max_length = 30)
    path = models.FileField(upload_to = 'media')
    user = models.ForeignKey(get_user_model(),  on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    comment = models.CharField(max_length = 300)
    analysis = models.CharField(max_length = 6)
    data_id = models.IntegerField()
    created_at = models.CharField(max_length = 40)

    def __str__(self):
        return self.comment

