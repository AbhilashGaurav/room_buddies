from django.shortcuts import render
from django.http import HttpResponse

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