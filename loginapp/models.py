from datetime import datetime
from django.db import models

# Create your models here.
class Sysusers(models.Model):
    user_id = models.AutoField(max_length=11, primary_key=True)
    account = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=15)
    nickname = models.CharField(max_length=255)
    age = models.IntegerField(max_length=3,default=18)
    gender = models.IntegerField(max_length=1, default=1)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=40)
    addtime = models.DateTimeField(max_length=6, default=datetime.now)
    type = models.IntegerField(max_length=1,default=0)
    class Meta:
        db_table = "sysusers"