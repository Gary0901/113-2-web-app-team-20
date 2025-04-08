from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

def home(request):
    # 處理表單提交
    if request.method == 'POST':
        # 獲取表單數據
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        drink = request.POST.get('drink', '')
        size = request.POST.get('size', '')
        
        # 獲取配料列表
        toppings = request.POST.getlist('toppings', [])
        notes = request.POST.get('notes', '')
        
        # 在實際應用中，這裡可以將數據保存到數據庫
        # 例如：Order.objects.create(name=name, phone=phone, ...)
        
        # 添加成功消息
        messages.success(request, '訂單已成功提交！我們會盡快處理您的訂單。')
        
        # 重定向到主頁，避免表單重複提交
        return redirect('home')
    
    # 設定周年慶日期
    anniversary_date = datetime.datetime(2025, 4, 15)
    
    # 計算距離周年慶還有多少天
    today = datetime.datetime.now()
    time_left = anniversary_date - today
    
    # 計算天數、小時、分鐘、秒數
    days = time_left.days
    hours = (time_left.seconds // 3600) 
    minutes = (time_left.seconds % 3600) // 60
    seconds = time_left.seconds % 60
    
    # 如果活動已開始，設定適當的消息
    countdown_message = "活動即將開始，敬請期待！"
    if time_left.total_seconds() <= 0:
        countdown_message = "周年慶活動進行中！"
        days, hours, minutes, seconds = 0, 0, 0, 0
    
    # 輪播的圖片和標題
    banner_images = [
        "drink1.jpg",
        "drink2.jpg", 
        "drink3.jpg",
    ]
    
    banner_titles = [
        "春季新品上市", 
        "夏季特惠活動",
        "周年慶即將到來"
    ]
    
    # 準備菜單內容
    menu_items = [
        {
            'category': '人氣茶飲',
            'items': [
                {'name': '珍珠奶茶', 'image': 'bubble.jpg', 'description': '經典台灣風味，香濃奶茶搭配QQ珍珠', 'price': 60},
                {'name': '芒果綠茶', 'image': 'mango.jpg', 'description': '新鮮芒果果肉，搭配甘甜綠茶', 'price': 75},
                {'name': '鮮奶茶', 'image': 'milktea.jpg', 'description': '使用高品質鮮奶，香醇茶香完美結合', 'price': 65},
            ]
        },
        {
            'category': '特調飲品',
            'items': [
                {'name': '繽紛水果茶', 'image': 'fruit.jpg', 'description': '多種新鮮水果，清爽的水果茶基底', 'price': 85},
                {'name': '抹茶拿鐵', 'image': 'mocha.jpg', 'description': '日本進口抹茶粉，搭配濃郁鮮奶', 'price': 80},
                {'name': '檸檬冬瓜茶', 'image': 'lemontea.jpg', 'description': '清甜冬瓜茶加上新鮮檸檬片', 'price': 70},
            ]
        }
    ]
    
    # 準備價格表
    price_table = [
        {'category': '基本茶飲', 'medium': 50, 'large': 60},
        {'category': '鮮奶茶系列', 'medium': 65, 'large': 75},
        {'category': '水果茶系列', 'medium': 70, 'large': 85},
    ]
    
    context = {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'countdown_message': countdown_message,
        'banner_images': banner_images,
        'banner_titles': banner_titles,
        'current_banner_index': 0,  # 初始顯示的輪播索引
        'menu_items': menu_items,
        'price_table': price_table,
    }
    
    return render(request, 'drink_shop/home.html', context)