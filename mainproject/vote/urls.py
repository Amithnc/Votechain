from django.urls import path
from . import views

urlpatterns=[
    path('capture',views.homepage,name='homepage'),
    path('train/',views.train,name="train-model"),
    path('recoginze',views.recoginze_face,name='recoginze_face'),
]