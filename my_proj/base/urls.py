<<<<<<< HEAD
from django.urls import path
from . import views
urlpatterns =[
    path("login/",views.loginPage,name="login"),
    path("logout/",views.logoutUser,name="logout"),
    path("register/",views.registerPage,name="register"),

    path("",views.home,name="home"),
    path("room/<str:pk>/",views.room,name="room"),

    path("create-room/",views.createRoom,name="create-room"),
    path("update-room/<str:pk>/",views.updateRoom,name="update-room"),
    path("delete-room/<str:pk>/",views.delete_room,name="delete-room"),
=======
from django.urls import path
from . import views
urlpatterns =[
    path("login/",views.loginPage,name="login"),
    path("logout/",views.logoutUser,name="logout"),
    path("register/",views.registerPage,name="register"),

    path("",views.home,name="home"),
    path("room/<str:pk>/",views.room,name="room"),

    path("create-room/",views.createRoom,name="create-room"),
    path("update-room/<str:pk>/",views.updateRoom,name="update-room"),
    path("delete-room/<str:pk>/",views.delete_room,name="delete-room"),
>>>>>>> 7473195b0f73cdab975da524bc95679a4926a05b
]  