# store/admin.py
from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}   # auto-fills slug from name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display         = ['name', 'category', 'price', 'badge', 'in_stock', 'is_featured']
    list_filter          = ['category', 'badge', 'in_stock', 'is_featured']
    list_editable        = ['price', 'badge', 'in_stock', 'is_featured']   # edit inline!
    search_fields        = ['name', 'description']