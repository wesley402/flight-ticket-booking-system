from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile

# Create your models here.
class Airline(models.Model):
    id = models.CharField(primary_key=True, max_length=2, blank=False)
    name = models.CharField(max_length=100)

class Airport(models.Model):
    id = models.CharField(primary_key=True, max_length=3, blank=False)
    name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=40, blank=True)

class Route(models.Model):
    flight_no = models.IntegerField(null=True)
    stop_no = models.IntegerField(null=True)
    airline_id = models.CharField(max_length= 4, blank=True)
    src_airport = models.CharField(max_length=4, blank=True)
    dst_airport = models.CharField(max_length=4, blank=True)
    num_of_seats = models.IntegerField(null=True)
    num_of_stops = models.IntegerField(null=True)
    src_time = models.TimeField(null=True)
    dst_time = models.TimeField(null=True)
    arrive_day = models.IntegerField(null=True)
    working_days = models.CharField(max_length=40, blank=True)
    fare = models.FloatField(null=True)
    fare_restriction = models.CharField(max_length=40, blank=True)
    flying_time = models.TimeField(null=True)
    #airline_id = models.ForeignKey(Airline, related_name='airline_route_id', on_delete=models.CASCADE)
    #src_airport = models.ForeignKey(Airport, related_name='airport_route_id', on_delete=models.CASCADE)
    #dst_airport = models.ForeignKey(Airport, related_name='airport_id', on_delete=models.CASCADE)

class CustomerManager(models.Manager):
    def get_queryset(self):
        return super(CustomerManager, self).get_queryset().filter(
            is_staff=0)

class Customers(User):
    objects = CustomerManager()
    class Meta:
        proxy = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

class CustomerProfiles(Customers):
    class Meta:
        proxy = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
