from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('register/',views.register),
    path('capture/',views.capture_images),
    path('train/',views.train,name="train-model"),
    path('recoginze/',views.recoginze_face,name='recoginze_face'),
    path('api/',views.api),
]