from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Call(models.Model):
    message = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.message
