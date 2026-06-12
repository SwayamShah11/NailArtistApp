from django.urls import path

from .views import (
    appointment_list,
    appointment_create
)

urlpatterns = [

    path(
        '',
        appointment_list,
        name='appointment_list'
    ),

    path(
        'create/',
        appointment_create,
        name='appointment_create'
    ),
]