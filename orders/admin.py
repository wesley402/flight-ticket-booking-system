from django.contrib import admin
from .models import Reservation, Leg

# Register your models here.
class ReservationModelAdmin(admin.ModelAdmin):

    list_display = (
    'reservation_no',
    'reservation_date',
    'reservation_status',
    'username',
    'num_legs',
    'fare_restrictions',
    'passengers',
    'booking_fee',
    'total_fare',
    'customer_rep',
    'num_of_psgs',
    )

    list_filter = (
    'reservation_no',
    'reservation_date',
    'reservation_status',
    'username',
    'num_legs',
    'fare_restrictions',
    'passengers',
    'booking_fee',
    'total_fare',
    'customer_rep',
    'num_of_psgs',
    )
    
class LegModelAdmin(admin.ModelAdmin):

    list_display = (
    'id',
    'reservation_no',
    'leg_no',
    'airline_id',
    'flight_no',
    'src_time',
    'src_airport',
    'dst_time',
    'dst_airport',
    'cabin',
    )

    list_filter = (
    'reservation_no',
    'src_airport',
    'dst_airport',
    )

admin.site.register(Reservation, ReservationModelAdmin)
admin.site.register(Leg, LegModelAdmin)
