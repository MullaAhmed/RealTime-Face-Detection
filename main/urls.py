from django.urls import path,include
from .views import *
urlpatterns = [

    path('',With_0,name='0'),
    path('1',With_1,name='1')

]
