from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('register/',views.register),
    path('capture/<str:id>',views.capture_images),
    path('train/',views.train,name="train-model"),
    path('recoginze/<int:id>',views.recoginze_face,name='recoginze_face'),
]