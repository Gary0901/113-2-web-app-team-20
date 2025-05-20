from django.db import models
from django.contrib.auth.models import User
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
    
    member = models.ForeignKey(
        'Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders',
        verbose_name='會員'
    )

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
    


class Member(models.Model):
    """會員模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    phone = models.CharField('手機號碼', max_length=20)
    points = models.IntegerField('積分', default=0)
    
    # 可選：會員等級
    LEVEL_CHOICES = [
        ('bronze', '銅卡會員'),
        ('silver', '銀卡會員'),
        ('gold', '金卡會員'),
    ]
    level = models.CharField('會員等級', max_length=10, choices=LEVEL_CHOICES, default='bronze')
    
    # 會員註冊時間
    created_at = models.DateTimeField('註冊時間', auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_level_display()}"
    
    def update_level(self):
        """根據積分更新會員等級"""
        if self.points >= 500:
            self.level = 'gold'
        elif self.points >= 200:
            self.level = 'silver'
        else:
            self.level = 'bronze'
        self.save()
        
class Comment(models.Model):
    """評論模型"""
    # 評論ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # 評論者資訊
    nickname = models.CharField('暱稱', max_length=50, default='匿名用戶')
    
    # 評論內容
    message = models.TextField('評論內容', null=False)
    
    # 刪除密碼
    del_pass = models.CharField('刪除密碼', max_length=50)
    
    # 評論時間
    pub_time = models.DateTimeField('發布時間', auto_now_add=True)
    
    # 評論狀態
    enabled = models.BooleanField('是否顯示', default=False)
    
    # 相關聯的飲品
    drink = models.CharField('飲品', max_length=50, choices=Order.DRINK_CHOICES)
    
    # 評分 (1-5星)
    RATING_CHOICES = [
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星'),
    ]
    rating = models.IntegerField('評分', choices=RATING_CHOICES, default=5)
    
    # 關聯會員 (可選)
    member = models.ForeignKey(
        'Member', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='comments',
        verbose_name='會員'
    )
    
    def __str__(self):
        """提供評論的字符串表示"""
        return f'{self.nickname} - {self.get_drink_display()} ({self.pub_time.strftime("%Y-%m-%d %H:%M")})'
    
    class Meta:
        verbose_name = '評論'
        verbose_name_plural = '評論'
        ordering = ['-pub_time']  # 按評論時間倒序排列