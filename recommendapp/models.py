from django.db import models

# Create your models here.
class Checkins(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user_id = models.IntegerField(max_length=11)
    venue_id = models.IntegerField(max_length=11)
    latitude = models.FloatField()
    longitude = models.FloatField()
    create_at = models.DateField(max_length=255)
    class Meta:
        db_table = "checkins"

class Users(models.Model):
    user_id = models.IntegerField(max_length=11)
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    class Meta:
        db_table = "users"

class Venues(models.Model):
    venue_id = models.IntegerField(max_length=11,primary_key=True)
    venue_name = models.CharField(max_length=40)
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    introducoty = models.CharField(max_length=255,default="暂无介绍")
    class Meta:
        db_table = "venues"

class Venuetopic(models.Model):
    venue_id = models.FloatField(max_length=20,primary_key=True)
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    venue_category = models.IntegerField(max_length=11)
    topic = models.IntegerField(max_length=20)
    class Meta:
        db_table = "venuetopic"

class Ratings(models.Model):
    user_id = models.IntegerField(max_length=255)
    venue_id = models.IntegerField(max_length=255)
    rating = models.FloatField(max_length=11)
    class Meta:
        db_table = "ratings"

class Venueflection(models.Model):
    venue_id = models.FloatField(primary_key=True)
    venue_name = models.CharField(max_length=255)
    class Meta:
        db_table = "venueflection"