from django.urls import path
from post import views
 
urlpatterns =[
    path('',views.index,name='index')
]