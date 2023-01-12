from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import RoomForm
# Create your views here.
from .models import Room
rooms = [
    {'id': 1, 'name': '1 oop data'},
    {'id': 2, 'name': '2 data'},
    {'id': 3, 'name': '3 data'},
    {'id': 4, 'name': '4 data'}
]
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    # room =None
    # for i in rooms:
    #     if i['id'] ==int(pk):
    #         room =i
    context = {'room':room}
    return render(request, 'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request,"base/room_form.html",context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request,"base/room_form.html",context)