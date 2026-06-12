from django.contrib import admin
from .models import Category, NailDesign, SavedDesign


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(NailDesign)
class NailDesignAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'category',
        'created_at'
    ]


@admin.register(SavedDesign)
class NailDesignAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'design',
        'created_at'
    ]
