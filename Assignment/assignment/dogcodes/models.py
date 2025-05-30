from django.db import models
from django.contrib.auth.models import User

class ResponseList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ResponseCode(models.Model):
    list = models.ForeignKey(ResponseList, related_name='codes', on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    image_url = models.URLField()

    def __str__(self):
        return self.code