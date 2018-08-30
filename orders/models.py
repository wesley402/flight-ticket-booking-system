from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    RESERVATION_STATUS = (
        ('A','Accepted'),
        ('C','Cancelled'),
    )
    reservation_no = models.CharField(max_length=100, blank=True, primary_key=True)
    reservation_date = models.DateTimeField(auto_now_add=True, blank=False)
    reservation_status = models.CharField(max_length=20, default = 'A', blank=False, choices=RESERVATION_STATUS)
    username = models.CharField(max_length=100, blank=True)
    num_legs = models.IntegerField(null=True)
    fare_restrictions = models.CharField(max_length=100, blank=True)
    passengers = models.CharField(max_length=100, blank=True)
    total_fare = models.FloatField(blank=True)
    booking_fee = models.FloatField(blank=True)
    customer_rep = models.CharField(max_length=25, blank=True)
    num_of_psgs = models.IntegerField(null=True)
    #customer_rep = models.ForeignKey(User,  to_field='username', on_delete=models.CASCADE)
    #username = models.ForeignKey(User,  to_field='username', on_delete=models.CASCADE)



class Leg(models.Model):
    reservation_no = models.CharField(max_length=100, blank=True)
    leg_no = models.IntegerField(null=True)
    airline_id = models.CharField(max_length=3, blank=True)
    flight_no = models.IntegerField(null=True)
    stop_no = models.IntegerField(null=True)
    seat_num = models.IntegerField(null=True)
    src_time = models.DateTimeField(blank=True)
    dst_time = models.DateTimeField(blank=True)
    cabin = models.CharField(max_length=20, blank=True)
    meal_preference = models.CharField(max_length=100, blank=True)
    src_airport = models.CharField(max_length=4, blank=True)
    dst_airport = models.CharField(max_length=4, blank=True)
