from django.urls import path
from .views import supplier_list, supplier_create


urlpatterns = [
    path('', supplier_list, name='supplier_list'),
    path('create/', supplier_create, name='supplier_create'),
]