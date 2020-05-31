from datetime import datetime
from time import strptime

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View

from reservation.models import Room, Reserve


class ListAllRooms(View):

    def post(self, request):
        return ListAllRooms.helper(self, request)

    def get(self, request):
        return ListAllRooms.helper(self, request)

    def helper(self, request):
        if Room.objects.all():
            return render(request, "list_rooms.html", {'rooms': Room.objects.all()})
        else:
            return render(request, "list_rooms.html", {'msg': 'Brak dostepnych sal'})


class AddOrModifyRoom(View):

    def post(self, request, id=0):
        if id == 0:
            r = Room()
        else:
            r = Room.objects.get(pk=id)
        flag = False
        r.has_projector = request.POST['has_projector']
        capacity = request.POST['capacity']
        if capacity:
            if int(capacity) >= 0:
                r.capacity = capacity
            else:
                messages.error(request, "Capacity cant be less than 0.")
                flag = True
        else:
            messages.error(request, 'Dont leave capacity field empty!')
            flag = True
        name = request.POST['name']
        if name:
            if name in Room.objects.all().values_list('name', flat=True):
                messages.error(request, 'Name already exists!')
                flag = True
            else:
                r.name = name
        else:
            messages.error(request, 'Name empty!')
            flag = True
        if flag:
            return render(request, 'room_form.html', {'room': r})
        else:
            r.save()
            messages.info(request, 'Zapisano!')
            return redirect('/')

    def get(self, request, id=0):
        if id == 0:
            return render(request, "room_form.html")
        else:
            return render(request, "room_form.html", {'room': Room.objects.get(pk=id)})


class DelRoom(View):

    def get(self, request, id):
        r = Room.objects.get(pk=id)
        return render(request, 'delete_object.html', {'obj': r})

    def post(self, request, id):
        r = Room.objects.get(pk=id)
        if request.POST['submit'] == "TAK":
            r.delete()
            messages.info(request, 'Usunieto!')
        return redirect('/')


class AddReserve(View):

    def get(self, request, id):
        r = Room.objects.get(pk=id)
        return render(request, "reserve.html", {'room': r, 'reservations': r.reserve_set.order_by('date')})

    def post(self, request, id):
        r = Reserve()
        comment = request.POST['comment']
        if comment:
            r.comment = comment
        date = request.POST['date']
        if date >= str(datetime.today().date()):
            r.date = date
        else:
            messages.error(request, "Nie mozna zarezerwowac na date z przeszlosci")
            return redirect(f'/room/reserve/{id}')
        r.room_id = Room.objects.get(pk=id)
        try:
            r.save()
        except IntegrityError as e:
            print('IntegrityError\n', e)
            messages.error(request, 'Sala jest juz tego dnia zajeta')
            return redirect(f'/room/reserve/{id}')
        messages.info(request, "Zarezerwowano!")
        return redirect('/')


class DetailRoom(View):

    def get(self, request, id):
        r = Room.objects.get(pk=id)
        return render(request, 'room_details.html', {'room': r, 'reservations': r.reserve_set.order_by('date')})


class Search(View):

    def get(self, request):
        return render(request, 'room_form.html')

    def post(self, request):
        name = request.POST['name']
        date = request.POST['date']
        has_projector = request.POST['has_projector']

        search = ''
        if name:
            pass

