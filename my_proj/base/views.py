from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
rooms = [
    {'id': 1, 'name': '1 oop data'},
    {'id': 2, 'name': '2 data'},
    {'id': 3, 'name': '3 data'},
]
def home(request):
    return render(request, 'base/home.html',{'rooms':rooms})

def room(request,pk):
    return render(request, 'base/room.html')