from django.db import models

class Order(models.Model):
    """訂單模型"""
    
    # 客戶信息
    name = models.CharField('姓名', max_length=100)
    phone = models.CharField('電話', max_length=20)
    
    # 飲品選擇
    DRINK_CHOICES = [
        ('bubble-tea', '珍珠奶茶'),
        ('mango-green-tea', '芒果綠茶'),
        ('milk-tea', '鮮奶茶'),
        ('fruit-tea', '繽紛水果茶'),
        ('matcha-latte', '抹茶拿鐵'),
        ('lemon-winter-melon', '檸檬冬瓜茶'),
    ]
    drink = models.CharField('飲品', max_length=50, choices=DRINK_CHOICES)
    
    # 杯型選擇
    SIZE_CHOICES = [
        ('medium', '中杯'),
        ('large', '大杯'),
    ]
    size = models.CharField('杯型', max_length=10, choices=SIZE_CHOICES)
    
    # 配料選擇（以逗號分隔的字符串存儲）
    toppings = models.CharField('配料', max_length=100, blank=True)
    
    # 備註
    notes = models.TextField('備註', blank=True)
    
    # 訂單時間
    created_at = models.DateTimeField('下單時間', auto_now_add=True)
    
    def __str__(self):
        """提供訂單的字符串表示"""
        return f'{self.name} - {self.get_drink_display()} ({self.created_at.strftime("%Y-%m-%d %H:%M")})'
    
    class Meta:
        verbose_name = '訂單'
        verbose_name_plural = '訂單'
        ordering = ['-created_at']  # 按下單時間倒序排列