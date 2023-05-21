from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User
# from django.contrib.auth.models import User

from .forms import RoomForm ,UserForm, MyUserCreationForm

# Create your views here.
# rooms = [
#     {'id': 1, 'name': '1 oop data'},
#     {'id': 2, 'name': '2 data'},
#     {'id': 3, 'name': '3 data'},
#     {'id': 4, 'name': '4 data'}
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Invalid username or password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password does not exist')
    context = {'page': page}
    return render(request,"base/login_register.html",context)

def  logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

    form  = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request,'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()
    # room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': rooms_count,'room_messages': room_messages} 
    return render(request, 'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    # room =None
    # for i in rooms:
    #     if i['id'] ==int(pk):
    #         room =i
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(user = request.user,room = room,body = request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages =user.message_set.all()
    topics =Topic.objects.all()
    context={'user': user, 'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

# create a new room 
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # print(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room =form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request,"base/room_form.html",context)

# update the authorized room
@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user !=room.host:
        return HttpResponse('You are not allowed here!!!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        
        return redirect('home')
    context = {'form': form,'topics': topics,'room': room}
    return render(request,"base/room_form.html",context)


# delete an authorized room
@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user !=room.host:
        return HttpResponse('You are not allowed here!!!')
    if request.method =='POST':
        room.delete()
        return redirect('home')
    return render(request,"base/delete.html",{'obj':room})

# delete messages
@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!!')
    if request.method =='POST':
        message.delete()
        return redirect('home')
    return render(request,"base/delete.html",{'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form =UserForm(instance =user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)

    return render(request,"base/update_user.html",{'form':form})

def  topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    topics = Topic.objects.filter(name__icontains=q)
    return render(request,"base/topics.html",{'topics':topics})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,"base/activity.html",{'room_messages': room_messages})