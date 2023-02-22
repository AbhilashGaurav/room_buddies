<<<<<<< HEAD

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('base.urls')),
    # path("", base),
    # path("room/",room),
]
=======

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('base.urls')),
    # path("", base),
    # path("room/",room),
]
>>>>>>> 7473195b0f73cdab975da524bc95679a4926a05b
