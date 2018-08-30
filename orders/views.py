from django.shortcuts import render
from .models import Reservation, Leg
from django.http import HttpResponse
from django.core.cache import cache
from datetime import datetime, timedelta
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages

import random

# Create your views here.
def checkout(request):
    if request.method == 'POST':
        now = datetime.now()
        reserv_no = 'TX' + now.strftime('%Y%m%d%H%M%S%f')
        ppls = ''
        for i in range(int(request.session['num_of_psgs'])):
            first_name = 'first_name' + str(i)
            last_name = 'last_name' + str(i)
            ppls = ppls + request.POST[first_name] + ' ' + request.POST[last_name] + ','

        if request.session['trip'] == 'oneway':


            raw_dep_date = request.session['raw_dep_date']
            dep_date = datetime.strptime(raw_dep_date, '%m/%d/%Y')

            Reservation.objects.create(
                username=request.user.username,
                reservation_no=reserv_no,
                num_legs= int(request.session['num_of_stops']) + 1,
                fare_restrictions='',
                passengers = ppls,
                total_fare = float(request.session['total_fare']),
                booking_fee = float(request.session['booking_fee']),
                customer_rep ='wesley',
                num_of_psgs= int(request.session['num_of_psgs']))

            if request.session['num_of_stops'] == '0':

                order_direct_flight = cache.get('order_direct_flight')
                add_day = timedelta(days=order_direct_flight[8])

                Leg.objects.create(
                    reservation_no=reserv_no,
                    leg_no = 1,
                    airline_id = order_direct_flight[0],
                    flight_no = order_direct_flight[1],
                    src_airport = order_direct_flight[2],
                    dst_airport = order_direct_flight[3],
                    src_time = dep_date.strftime('%Y-%m-%d') + ' ' + order_direct_flight[4].strftime('%H:%M'),
                    dst_time = (dep_date + add_day).strftime('%Y-%m-%d') + ' ' + order_direct_flight[5].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                )

            else:#if request.session['trip'] == 'oneway' and request.session['num_of_stops'] == '1':

                order_onestop_flight = cache.get('order_onestop_flight')
                add_day1 = timedelta(days=order_onestop_flight[8])
                add_day2 = timedelta(days=order_onestop_flight[17])
                Leg.objects.create(
                    reservation_no = reserv_no,
                    leg_no = 1,
                    airline_id = order_onestop_flight[0],
                    flight_no = order_onestop_flight[1],
                    src_airport = order_onestop_flight[2],
                    dst_airport = order_onestop_flight[3],
                    src_time = dep_date.strftime('%Y-%m-%d') + ' ' + order_onestop_flight[4].strftime('%H:%M'),
                    dst_time = (dep_date + add_day1).strftime('%Y-%m-%d') + ' ' + order_onestop_flight[5].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                )
                Leg.objects.create(
                    reservation_no = reserv_no,
                    leg_no = 2,
                    airline_id = order_onestop_flight[9],
                    flight_no = order_onestop_flight[10],
                    src_airport = order_onestop_flight[11],
                    dst_airport = order_onestop_flight[12],
                    src_time = (dep_date + add_day1).strftime('%Y-%m-%d') + ' ' + order_onestop_flight[13].strftime('%H:%M'),
                    dst_time = (dep_date + add_day1 + add_day2).strftime('%Y-%m-%d') + ' ' + order_onestop_flight[14].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                    )
            message = "Your Order Succeed!!!!!!!!!!!"
            return render(request, 'message.html',{'message' : message})
            
        else:#roundtrip
            raw_dep_date = request.session['raw_dep_date']
            raw_rtn_date = request.session['raw_dep_date']

            dep_date = datetime.strptime(raw_dep_date, '%m/%d/%Y')
            rtn_date = datetime.strptime(raw_rtn_date, '%m/%d/%Y')

            Reservation.objects.create(
                username=request.user.username,
                reservation_no=reserv_no,
                num_legs= int(request.session['dst_num_of_stops']) + 1 + int(request.session['rtn_num_of_stops']) + 1,
                fare_restrictions='',
                passengers = ppls,
                total_fare = float(request.session['total_fare']),
                booking_fee = float(request.session['booking_fee']),
                customer_rep ='wesley',
                num_of_psgs= int(request.session['num_of_psgs']))

            # Store dst trip to database
            if request.session['dst_num_of_stops'] == '0':

                dst_order_flight = cache.get('dst_order_flight')
                add_day = timedelta(days=dst_order_flight[8])

                Leg.objects.create(
                    reservation_no=reserv_no,
                    leg_no = 1,
                    airline_id = dst_order_flight[0],
                    flight_no = dst_order_flight[1],
                    src_airport = dst_order_flight[2],
                    dst_airport = dst_order_flight[3],
                    src_time = dep_date.strftime('%Y-%m-%d') + ' ' + dst_order_flight[4].strftime('%H:%M'),
                    dst_time = (dep_date + add_day).strftime('%Y-%m-%d') + ' ' + dst_order_flight[5].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                )

            else:

                dst_order_flight = cache.get('dst_order_flight')
                add_day1 = timedelta(days=dst_order_flight[8])
                add_day2 = timedelta(days=dst_order_flight[17])
                Leg.objects.create(
                    reservation_no = reserv_no,
                    leg_no = 1,
                    airline_id = dst_order_flight[0],
                    flight_no = dst_order_flight[1],
                    src_airport = dst_order_flight[2],
                    dst_airport = dst_order_flight[3],
                    src_time = dep_date.strftime('%Y-%m-%d') + ' ' + dst_order_flight[4].strftime('%H:%M'),
                    dst_time = (dep_date + add_day1).strftime('%Y-%m-%d') + ' ' + dst_order_flight[5].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                )
                Leg.objects.create(
                    reservation_no = reserv_no,
                    leg_no = 2,
                    airline_id = dst_order_flight[9],
                    flight_no = dst_order_flight[10],
                    src_airport = dst_order_flight[11],
                    dst_airport = dst_order_flight[12],
                    src_time = (dep_date + add_day1).strftime('%Y-%m-%d') + ' ' + dst_order_flight[13].strftime('%H:%M'),
                    dst_time = (dep_date + add_day1 + add_day2).strftime('%Y-%m-%d') + ' ' + dst_order_flight[14].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                    )

            # Store RTN trip to database
            if request.session['rtn_num_of_stops'] == '0':

                rtn_order_flight = cache.get('rtn_order_flight')
                add_day = timedelta(days=rtn_order_flight[8])

                Leg.objects.create(
                    reservation_no=reserv_no,
                    leg_no = 3,
                    airline_id = rtn_order_flight[0],
                    flight_no = rtn_order_flight[1],
                    src_airport = rtn_order_flight[2],
                    dst_airport = rtn_order_flight[3],
                    src_time = rtn_date.strftime('%Y-%m-%d') + ' ' + rtn_order_flight[4].strftime('%H:%M'),
                    dst_time = (rtn_date + add_day).strftime('%Y-%m-%d') + ' ' + rtn_order_flight[5].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                )

            else:#if request.session['trip'] == 'oneway' and request.session['num_of_stops'] == '1':

                rtn_order_flight = cache.get('rtn_order_flight')
                add_day1 = timedelta(days=rtn_order_flight[8])
                add_day2 = timedelta(days=rtn_order_flight[17])
                Leg.objects.create(
                    reservation_no = reserv_no,
                    leg_no = 3,
                    airline_id = rtn_order_flight[0],
                    flight_no = rtn_order_flight[1],
                    src_airport = rtn_order_flight[2],
                    dst_airport = rtn_order_flight[3],
                    src_time = rtn_date.strftime('%Y-%m-%d') + ' ' + rtn_order_flight[4].strftime('%H:%M'),
                    dst_time = (rtn_date + add_day1).strftime('%Y-%m-%d') + ' ' + rtn_order_flight[5].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                )
                Leg.objects.create(
                    reservation_no = reserv_no,
                    leg_no = 4,
                    airline_id = rtn_order_flight[9],
                    flight_no = rtn_order_flight[10],
                    src_airport = rtn_order_flight[11],
                    dst_airport = rtn_order_flight[12],
                    src_time = (rtn_date + add_day1).strftime('%Y-%m-%d') + ' ' + rtn_order_flight[13].strftime('%H:%M'),
                    dst_time = (rtn_date + add_day1 + add_day2).strftime('%Y-%m-%d') + ' ' + rtn_order_flight[14].strftime('%H:%M'),
                    cabin = request.session['cabin'],
                    seat_num = random.randint(0, 100),
                    )

            message = "Your Order Succeed!!!!!!!!!!!"
            return render(request, 'message.html',{'message' : message})







    else:
        num_of_psgs = int(request.session['num_of_psgs'])
        return render(request, 'orders/checkout.html', {'range':range(num_of_psgs)})

def order(request):
    return render(request, 'orders/order.html')


def history_order(request):
    if request.method == 'POST':
        if 'detail' in request.POST:
            order_no = request.POST['detail']
            print(order_no)
            cursor = connection.cursor()
            cursor.callproc('getOrderDetail', [request.user.username, order_no])
            travel_tuples = cursor.fetchall()
            cursor.close()
            print(travel_tuples)
            return render(request, 'orders/order_detail.html', {'travel_tuples': travel_tuples})

    orderLists = Reservation.objects.filter(username=request.user.username)
    if orderLists.exists():
        return render(request, 'orders/history_order.html', {'orderLists': orderLists})
    else:
        return HttpResponse("<h>No Order History Exists !!!!!!</h>")
def current_order(request):
    if request.method == 'POST':
            if 'detail' in request.POST:
                order_no = request.POST['detail']
                print(order_no)
                cursor = connection.cursor()
                cursor.callproc('getOrderDetail', [request.user.username,order_no])
                travel_tuples = cursor.fetchall()
                cursor.close()
                print(travel_tuples)
                return render(request, 'orders/order_detail.html', {'travel_tuples': travel_tuples})

            if 'cancel' in request.POST:
                order_no = request.POST['cancel']
                cursor = connection.cursor()
                cursor.callproc('cancelReservation', [request.user.username, order_no])
                cursor.close()
                return redirect('/order/current-order')

    else:
        currOrderLists = Reservation.objects.filter(reservation_status='A', username=request.user.username)
        if currOrderLists.exists():
            return render(request, 'orders/current_order.html', {'currOrderLists': currOrderLists})
        else:
            return HttpResponse("<h>No Current Order Exists !!!!!!</h>")
