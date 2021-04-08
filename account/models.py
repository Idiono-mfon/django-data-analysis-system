from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.
class CustomUser(AbstractUser):
    # username = models.CharField().unique
    name = models.CharField(max_length= 20)
    email = models.EmailField(max_length = 100)
    created_at = models.DateTimeField(auto_now=True)
    access_code = models.CharField(max_length = 40)
    def __str__(self):
        return self.username
      