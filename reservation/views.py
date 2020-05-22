from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from reservation.models import Room


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
            return render(request, 'room.html', {'room': r})
        else:
            r.save()
            messages.info(request, 'Zapisano!')
            return redirect('/')

    def get(self, request, id=0):
        if id == 0:
            return render(request, "room.html")
        else:
            return render(request, "room.html", {'room': Room.objects.get(pk=id)})


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
