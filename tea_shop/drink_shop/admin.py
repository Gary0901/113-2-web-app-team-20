from django.contrib import admin
from .models import Order, Comment, Member  # 確保引入 Comment 模型

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """訂單管理介面配置"""
    list_display = ('name', 'phone', 'get_drink_display', 'size', 'toppings', 'created_at')
    list_filter = ('drink', 'size', 'created_at')
    search_fields = ('name', 'phone', 'notes')
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """評論管理界面配置"""
    list_display = ('nickname', 'drink', 'rating', 'message', 'enabled', 'pub_time')
    list_filter = ('drink', 'rating', 'enabled', 'pub_time')
    search_fields = ('nickname', 'message')
    date_hierarchy = 'pub_time'
    list_editable = ('enabled',)  # 允許直接在列表中編輯啟用狀態