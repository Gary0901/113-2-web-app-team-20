from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order  # 導入訂單模型
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MemberSerializer, RegisterSerializer, OrderSerializer
from .models import Member
from django.contrib.auth.models import User
import datetime

from .forms import CommentForm  # 確保引入表單
from .models import Comment
from django.shortcuts import redirect, get_object_or_404

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
        
        # 將數據保存到數據庫
        toppings_str = ','.join(toppings) if toppings else ''
        order = Order.objects.create(
            name=name, 
            phone=phone, 
            drink=drink, 
            size=size, 
            toppings=toppings_str, 
            notes=notes
        )
        
         # 檢查是否有會員 Token 標頭
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            # 取得 token
            token = auth_header.split(' ')[1]
            try:
                # 驗證 token
                from rest_framework_simplejwt.tokens import AccessToken
                token_obj = AccessToken(token)
                user_id = token_obj['user_id']
                
                # 查找會員
                from django.contrib.auth.models import User
                user = User.objects.get(id=user_id)
                member = Member.objects.get(user=user)
                
                # 關聯訂單到會員
                order.member = member
                
                # 訂單完成後增加會員積分
                member.points += 10  # 每次訂購獲得 10 積分
                member.save()
                
                messages.success(request, f'訂單已成功提交！您獲得了 10 積分。您的訂單編號是 {order.id}')
            except Exception as e:
                # Token 驗證失敗
                messages.success(request, f'訂單已成功提交！您的訂單編號是 {order.id}')
        else:
            messages.success(request, f'訂單已成功提交！您的訂單編號是 {order.id}')
        
        # 保存訂單
        order.save()
        
        # 重定向到訂單狀態頁面
        return redirect('drink_shop:order_status', order_id=order.id)
    
    # 設定周年慶日期
    anniversary_date = datetime.datetime(2025, 6, 15)
    
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
        
    # 判斷是否在營業時間內
    current_hour = today.hour
    is_open = (current_hour >= 10 and current_hour < 22)
    
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
    
    # 準備菜單內容（加上 id 字段）
    menu_items = [
        {
            'category': '人氣茶飲',
            'items': [
                {'id': 'bubble-tea', 'name': '珍珠奶茶', 'image': 'bubble.jpg', 'description': '經典台灣風味，香濃奶茶搭配QQ珍珠', 'price': 60},
                {'id': 'mango-green-tea', 'name': '芒果綠茶', 'image': 'mango.jpg', 'description': '新鮮芒果果肉，搭配甘甜綠茶', 'price': 75},
                {'id': 'milk-tea', 'name': '鮮奶茶', 'image': 'milktea.jpg', 'description': '使用高品質鮮奶，香醇茶香完美結合', 'price': 65},
            ]
        },
        {
            'category': '特調飲品',
            'items': [
                {'id': 'fruit-tea', 'name': '繽紛水果茶', 'image': 'fruit.jpg', 'description': '多種新鮮水果，清爽的水果茶基底', 'price': 85},
                {'id': 'matcha-latte', 'name': '抹茶拿鐵', 'image': 'mocha.jpg', 'description': '日本進口抹茶粉，搭配濃郁鮮奶', 'price': 80},
                {'id': 'lemon-winter-melon', 'name': '檸檬冬瓜茶', 'image': 'lemontea.jpg', 'description': '清甜冬瓜茶加上新鮮檸檬片', 'price': 70},
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
        'is_open': is_open,  # 新增營業狀態
    }
    
    return render(request, 'drink_shop/home.html', context)

def menu(request):
    """顯示完整菜單頁面"""
    menu_items = [
        {
            'category': '人氣茶飲',
            'items': [
                {'id': 'bubble-tea', 'name': '珍珠奶茶', 'image': 'bubble.jpg', 'description': '經典台灣風味，香濃奶茶搭配QQ珍珠', 'price': 60},
                {'id': 'mango-green-tea', 'name': '芒果綠茶', 'image': 'mango.jpg', 'description': '新鮮芒果果肉，搭配甘甜綠茶', 'price': 75},
                {'id': 'milk-tea', 'name': '鮮奶茶', 'image': 'milktea.jpg', 'description': '使用高品質鮮奶，香醇茶香完美結合', 'price': 65},
            ]
        },
        {
            'category': '特調飲品',
            'items': [
                {'id': 'fruit-tea', 'name': '繽紛水果茶', 'image': 'fruit.jpg', 'description': '多種新鮮水果，清爽的水果茶基底', 'price': 85},
                {'id': 'matcha-latte', 'name': '抹茶拿鐵', 'image': 'mocha.jpg', 'description': '日本進口抹茶粉，搭配濃郁鮮奶', 'price': 80},
                {'id': 'lemon-winter-melon', 'name': '檸檬冬瓜茶', 'image': 'lemontea.jpg', 'description': '清甜冬瓜茶加上新鮮檸檬片', 'price': 70},
            ]
        }
    ]
    
    context = {
        'menu_items': menu_items,
    }
    return render(request, 'drink_shop/menu.html', context)

def category_detail(request, category):
    """顯示特定分類的飲品"""
    menu_items = [
        {
            'category': '人氣茶飲',
            'items': [
                {'id': 'bubble-tea', 'name': '珍珠奶茶', 'image': 'bubble.jpg', 'description': '經典台灣風味，香濃奶茶搭配QQ珍珠', 'price': 60},
                {'id': 'mango-green-tea', 'name': '芒果綠茶', 'image': 'mango.jpg', 'description': '新鮮芒果果肉，搭配甘甜綠茶', 'price': 75},
                {'id': 'milk-tea', 'name': '鮮奶茶', 'image': 'milktea.jpg', 'description': '使用高品質鮮奶，香醇茶香完美結合', 'price': 65},
            ]
        },
        {
            'category': '特調飲品',
            'items': [
                {'id': 'fruit-tea', 'name': '繽紛水果茶', 'image': 'fruit.jpg', 'description': '多種新鮮水果，清爽的水果茶基底', 'price': 85},
                {'id': 'matcha-latte', 'name': '抹茶拿鐵', 'image': 'mocha.jpg', 'description': '日本進口抹茶粉，搭配濃郁鮮奶', 'price': 80},
                {'id': 'lemon-winter-melon', 'name': '檸檬冬瓜茶', 'image': 'lemontea.jpg', 'description': '清甜冬瓜茶加上新鮮檸檬片', 'price': 70},
            ]
        }
    ]
    
    # 找到對應的分類
    category_data = next((item for item in menu_items if item['category'] == category), None)
    
    if category_data is None:
        # 處理分類不存在的情況
        messages.error(request, '找不到該分類的飲品')
        return redirect('drink_shop:home')
    
    context = {
        'category': category,
        'drinks': category_data['items'],
    }
    return render(request, 'drink_shop/category_detail.html', context)

def drink_detail(request, drink_slug):
    """顯示特定飲品的詳細資訊"""
    
    # 將 drink_slug 設為 drink_id，讓後面的代碼正常運作
    drink_id = drink_slug
    
    # 模擬查找飲品
    all_drinks = [
        {'id': 'bubble-tea', 'name': '珍珠奶茶', 'image': 'bubble.jpg', 'description': '經典台灣風味，香濃奶茶搭配QQ珍珠', 'price': 60},
        {'id': 'mango-green-tea', 'name': '芒果綠茶', 'image': 'mango.jpg', 'description': '新鮮芒果果肉，搭配甘甜綠茶', 'price': 75},
        {'id': 'milk-tea', 'name': '鮮奶茶', 'image': 'milktea.jpg', 'description': '使用高品質鮮奶，香醇茶香完美結合', 'price': 65},
        {'id': 'fruit-tea', 'name': '繽紛水果茶', 'image': 'fruit.jpg', 'description': '多種新鮮水果，清爽的水果茶基底', 'price': 85},
        {'id': 'matcha-latte', 'name': '抹茶拿鐵', 'image': 'mocha.jpg', 'description': '日本進口抹茶粉，搭配濃郁鮮奶', 'price': 80},
        {'id': 'lemon-winter-melon', 'name': '檸檬冬瓜茶', 'image': 'lemontea.jpg', 'description': '清甜冬瓜茶加上新鮮檸檬片', 'price': 70},
    ]
    
    drink = next((item for item in all_drinks if item['id'] == drink_id), None)
    
    if drink is None:
        messages.error(request, '找不到該飲品')
        return redirect('drink_shop:home')
    
    context = {
        'drink': drink,
    }
    return render(request, 'drink_shop/drink_detail.html', context)

def order_status(request, order_id):
    """查詢訂單狀態"""
    try:
        order = Order.objects.get(pk=order_id)
        
        # 準備額外的資料給 template 使用
        order.total_price = 0  # 計算總價
        order.base_price = 50  # 基本價格（可以根據飲品不同修改）
        
        if order.size == 'large':
            order.total_price = order.base_price + 10
        else:
            order.total_price = order.base_price
            
    except Order.DoesNotExist:
        messages.error(request, '找不到該訂單')
        return redirect('drink_shop:home')
    
    context = {
        'order': order,
    }
    return render(request, 'drink_shop/order_status.html', context)

def chatbot(request):
    """智能客服聊天界面"""
    return render(request, 'drink_shop/chatbot.html')

# 會員註冊 API
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "註冊成功！"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 會員資料 API (需要驗證)
class MemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            member = Member.objects.get(user=request.user)
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({"message": "會員資料不存在"}, status=status.HTTP_404_NOT_FOUND)

# 會員訂單歷史 API
class MemberOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.filter(name=request.user.username)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

def login(request):
    """會員登入頁面"""
    return render(request, 'drink_shop/login.html')

def register(request):
    """會員註冊頁面"""
    return render(request, 'drink_shop/register.html')

def member_center(request):
    """會員中心頁面"""
    return render(request, 'drink_shop/member_center.html')

def comments(request):
    """顯示評論頁面"""
    comments = Comment.objects.filter(enabled=True).order_by('-pub_time')
    comment_form = CommentForm()
    
    # 準備飲品數據用於展示
    all_drinks = [
        {'id': 'bubble-tea', 'name': '珍珠奶茶', 'image': 'bubble.jpg'},
        {'id': 'mango-green-tea', 'name': '芒果綠茶', 'image': 'mango.jpg'},
        {'id': 'milk-tea', 'name': '鮮奶茶', 'image': 'milktea.jpg'},
        {'id': 'fruit-tea', 'name': '繽紛水果茶', 'image': 'fruit.jpg'},
        {'id': 'matcha-latte', 'name': '抹茶拿鐵', 'image': 'mocha.jpg'},
        {'id': 'lemon-winter-melon', 'name': '檸檬冬瓜茶', 'image': 'lemontea.jpg'},
    ]
    
    drink_images = {drink['id']: drink['image'] for drink in all_drinks}
    
    return render(request, 'drink_shop/comments.html', {
        'comments': comments, 
        'comment_form': comment_form,
        'drink_images': drink_images,
        'is_open': True  # 添加營業狀態給base.html使用
    })

def post_comment(request):
    """處理評論提交"""
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 保存評論，但設置為未啟用狀態
            comment = comment_form.save(commit=False)
            
            # 檢查是否有會員Token
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                # 取得token
                token = auth_header.split(' ')[1]
                try:
                    # 驗證token
                    from rest_framework_simplejwt.tokens import AccessToken
                    token_obj = AccessToken(token)
                    user_id = token_obj['user_id']
                    
                    # 查找會員
                    from django.contrib.auth.models import User
                    user = User.objects.get(id=user_id)
                    member = Member.objects.get(user=user)
                    
                    # 關聯評論到會員
                    comment.member = member
                    
                    # 會員評論自動啟用
                    comment.enabled = True
                    
                    messages.success(request, '評論已成功提交！由於您是會員，評論已直接顯示。')
                except Exception as e:
                    # Token驗證失敗
                    messages.success(request, '評論已成功提交！待管理員審核後才會顯示。')
            else:
                messages.success(request, '評論已成功提交！待管理員審核後才會顯示。')
            
            comment.save()
            return redirect('drink_shop:comments')
        else:
            messages.error(request, '評論提交失敗！請檢查填寫的信息。')
    
    return redirect('drink_shop:comments')

def delete_comment(request, comment_id, del_pass):
    """刪除評論"""
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.del_pass == del_pass:
            comment.delete()
            messages.success(request, '評論已成功刪除！')
        else:
            messages.error(request, '密碼錯誤，無法刪除評論。')
    except:
        messages.error(request, '刪除評論時發生錯誤。')
    
    return redirect('drink_shop:comments')