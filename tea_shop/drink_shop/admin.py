from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """訂單管理介面配置"""
    list_display = ('name', 'phone', 'get_drink_display', 'size', 'toppings', 'created_at')
    list_filter = ('drink', 'size', 'created_at')
    search_fields = ('name', 'phone', 'notes')
    date_hierarchy = 'created_at'