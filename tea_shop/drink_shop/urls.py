from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'drink_shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('drinks/<str:category>/', views.category_detail, name='category_detail'),
    path('drink/<slug:drink_slug>/', views.drink_detail, name='drink_detail'),
    path('order/<uuid:order_id>/', views.order_status, name='order_status'),
    path('chatbot/', views.chatbot, name='chatbot'),

    # JWT 認證 API 路由
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/member/', views.MemberView.as_view(), name='member'),
    path('api/member/orders/', views.MemberOrdersView.as_view(), name='member_orders'),

    # 添加會員相關的 URL 路由
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('member/', views.member_center, name='member_center'),

    # 新增下面三個路徑
    path('comments/', views.comments, name='comments'),
    path('post_comment/', views.post_comment, name='post_comment'),
    path('delete_comment/<uuid:comment_id>/<str:del_pass>/', views.delete_comment, name='delete_comment'),
]