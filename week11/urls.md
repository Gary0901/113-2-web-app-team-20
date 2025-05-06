# Week08 作業報告 - 茶香飲品網站 (URL 路由優化)

## 1️⃣ 練習了哪些當週上課的主題

### 🔹 Django URLconf 進階管理
- 學習使用 `path()` 函數的進階功能，包含不同類型的路徑轉換器
- 掌握命名 URL 模式（URL patterns）的設計與應用
- 實作動態 URL 參數傳遞，支援多重參數組合

### 🔹 Path Converter 參數類型應用
- 使用 `<str:parameter>` 處理字串型參數
- 應用 `<int:parameter>` 處理整數型參數
- 實作 `<uuid:parameter>` 管理訂單查詢系統

### 🔹 URL 反解析機制
- 使用 `name` 參數為 URL 模式命名
- 在 views.py 中使用 `reverse()` 函數動態生成 URL
- 在模板中使用 `{% url %}` 標籤實現 URL 解析
- 利用 namespace 實現模組化路由管理

### 🔹 Include 功能的應用
- 使用 `include()` 將相關 URL 模式分組
- 實現應用程式級別的 URL 管理
- 設計清晰的 URL 結構層級

## 2️⃣ 額外找了與當週上課的主題相關的程式技術

### ✅ 重構茶店網站的 URL 架構
- 將飲品分類設計為動態路由：`/drinks/<category>/`
- 為每種飲品建立專屬頁面：`/drink/<drink_id>/`

### ✅ 實作 URL namespace 管理
```python
# tea_shop/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('drink_shop.urls')),
]

# drink_shop/urls.py
app_name = 'drink_shop'
urlpatterns = [
    path('', views.home, name='home'),
    path('drinks/<str:category>/', views.category_detail, name='category_detail'),
    path('drink/<str:drink_id>/', views.drink_detail, name='drink_detail'),
]

優化使用者體驗

實現分類瀏覽功能（點擊分類查看該類所有飲品）
建立飲品詳情頁面（顯示完整資訊與直接訂購選項）
完成訂單狀態查詢系統（用戶可查詢訂單進度）

實作成果展示
📍 新增的頁面與功能

飲品詳情頁面 (/drink/<drink_id>/)

顯示飲品完整資訊
提供即時訂購功能
包含麵包屑導航


分類瀏覽頁面 (/drinks/<category>/)

顯示特定分類的飲品
提供返回完整菜單的功能
