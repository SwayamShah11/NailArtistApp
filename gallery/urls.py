from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_list, name='gallery'),
    path(
        '<int:pk>/',
        views.design_detail,
        name='design_detail'
    ),
    path(
        'like/<int:pk>/',
        views.like_design,
        name='like_design'
    ),
    path(
        'save/<int:pk>/',
        views.save_design,
        name='save_design'
    ),
    path(
        'saved/',
        views.saved_designs,
        name='saved_designs'
    ),
    path(
        'unsave/<int:pk>/',
        views.unsave_design,
        name='unsave_design'
    ),
]