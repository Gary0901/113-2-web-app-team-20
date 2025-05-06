from django.db import models
import uuid

class Order(models.Model):
    """訂單模型"""
    
    # 訂單ID（使用UUID讓測試更清楚）
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
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
    
    # 新增：訂單狀態 - 用於測試 template 條件判斷
    STATUS_CHOICES = [
        ('pending', '待處理'),
        ('preparing', '製作中'),
        ('ready', '待取'),
        ('completed', '已完成'),
    ]
    status = models.CharField('訂單狀態', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        """提供訂單的字符串表示"""
        return f'{self.name} - {self.get_drink_display()} ({self.created_at.strftime("%Y-%m-%d %H:%M")})'
    
    @property
    def base_price(self):
        """基礎價格（用於測試 template filter）"""
        price_map = {
            'bubble-tea': 60,
            'mango-green-tea': 75,
            'milk-tea': 65,
            'fruit-tea': 85,
            'matcha-latte': 80,
            'lemon-winter-melon': 70,
        }
        return price_map.get(self.drink, 50)
    
    @property
    def total_price(self):
        """總價格（包含大杯加價）"""
        total = self.base_price
        if self.size == 'large':
            total += 10
        return total
    
    @classmethod
    def create_test_order(cls):
        """建立測試用訂單"""
        return cls.objects.create(
            name="測試用戶",
            phone="0912345678",
            drink="bubble-tea",
            size="large",
            toppings="珍珠,布丁",
            notes="這是一個測試用訂單，備註非常長的測試文字，用來測試 truncatechars filter 是否可以正確截斷長文字內容。",
            status="preparing"
        )
    
    @classmethod
    def create_multiple_test_orders(cls):
        """建立多個測試訂單"""
        orders = []
        for i in range(3):
            order = cls.objects.create(
                name=f"測試用戶 {i+1}",
                phone=f"09123456{i+10}",
                drink=cls.DRINK_CHOICES[i % len(cls.DRINK_CHOICES)][0],
                size=cls.SIZE_CHOICES[i % 2][0],
                toppings="珍珠" if i % 2 == 0 else "",
                notes=f"測試訂單 {i+1} 的備註內容",
                status=cls.STATUS_CHOICES[i % len(cls.STATUS_CHOICES)][0]
            )
            orders.append(order)
        return orders
    
    class Meta:
        verbose_name = '訂單'
        verbose_name_plural = '訂單'
        ordering = ['-created_at']  # 按下單時間倒序排列