# Week11 作業報告 - Django Template 實作

## 本週學習重點

### 1. Template 基礎語法
- 使用 `{{ }}` 語法顯示變數
- 使用 `{% %}` 控制結構（if, for）
- 實作條件判斷與迴圈

### 2. Template 繼承
- 建立 `base.html` 基礎模板
- 使用 `{% extends %}` 繼承基礎模板
- 定義 `{% block %}` 區塊供子模板覆蓋

### 3. Template Filter 應用
- 使用內建 filter 如 `date`, `truncatechars`, `floatformat`
- 在訂單狀態頁面格式化顯示資料

### 4. 靜態檔案管理
- 使用 `{% load static %}` 載入靜態檔案
- 正確引用 CSS 和圖片資源

## 主要實作內容

1. **Template 繼承結構**
   - 所有頁面繼承 `base.html`
   - 統一導航區、頁首、頁腳設計

2. **動態內容渲染**
   - 飲品菜單動態顯示
   - 價格表動態生成
   - 訂單狀態條件顯示

3. **時間相關功能**
   - 營業時間判斷
   - 周年慶倒數計時

4. **過濾器應用**
   - 日期格式化 `{{ created_at|date:"Y年m月d日" }}`
   - 價格格式化 `{{ price|floatformat:0 }}`
   - 文字截斷 `{{ text|truncatechars:50 }}`


## 下週計畫

- 學習 Custom Template Tags 和 Filters
- 實作更複雜的表單驗證
- 加入用戶認證功能

# Week11 作業報告 - 茶香飲品網站 (URL 路由優化)

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

實作成果展示
📍 新增的頁面與功能

飲品詳情頁面 (/drink/<drink_id>/)

顯示飲品完整資訊
提供即時訂購功能
包含麵包屑導航


分類瀏覽頁面 (/drinks/<category>/)

顯示特定分類的飲品
提供返回完整菜單的功能

## 3️⃣ 組員分工情況 (共100%)

| 組員     | 貢獻比例 | 負責內容                     |
|----------|----------|------------------------------|
| 蔡承燁   | 33.3%      | 額外主題相關的程式技術       |
| 章程睿   | 33.3%      | Django Template 實作及版本控制       |
| 陳皓偉   | 33.3%      | 茶香飲品網站 (URL 路由優化) - 當週上課的主題   |
