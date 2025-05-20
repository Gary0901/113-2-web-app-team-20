我們這個禮拜實作了三個功能如下:

# 茶香飲品評論區功能介紹

## 概述

本次實作的評論區功能是一個完整的使用者互動解決方案，讓顧客能夠對喜愛的飲品進行評價和分享心得。這個功能不僅豐富了網站的內容，也提供了寶貴的顧客反饋，幫助茶香飲品不斷改進產品質量和服務體驗。

## 技術架構

### 前端架構
- 使用 Django 模板系統處理頁面渲染
- 原生 JavaScript 處理用戶交互和表單驗證
- 響應式 CSS 設計適配不同設備
- 星級評分系統視覺化顧客評價

### 後端架構
- Django 網頁框架作為主要服務
- Django 表單系統處理數據驗證
- SQLite 資料庫存儲評論數據
- 自定義模板標籤擴展模板功能

### 數據流程
- 用戶提交評論表單
- 後端驗證並儲存評論
- 評論需經過管理員審核後顯示
- 會員評論可自動獲准顯示
- 用戶可通過密碼機制刪除自己的評論

## 關鍵功能

1. **評論發表**：用戶可以為指定飲品發表評論，包括評分和文字內容
2. **星級評分**：1-5星評分系統，直觀展示顧客對飲品的滿意度
3. **評論審核**：管理員可在後台審核評論，確保內容適當
4. **會員特權**：會員發表的評論自動獲准顯示，無需審核
5. **刪除機制**：評論者可通過設定的密碼刪除自己的評論
6. **評論展示**：美觀的評論卡片布局，清晰顯示評論者、時間和內容
7. **圖片整合**：每條評論自動關聯對應飲品的圖片

## 技術實現方式

評論區功能透過以下幾個關鍵技術組件實現：

1. **Django 模型設計**：自定義 Comment 模型儲存評論相關數據
2. **表單系統**：使用 Django ModelForm 簡化表單處理和驗證
3. **視圖函數**：處理評論展示、提交和刪除的邏輯
4. **模板設計**：美觀的評論列表和表單界面
5. **自定義過濾器**：使用模板標籤擴展模板功能
6. **會員系統集成**：與現有的 JWT 會員系統無縫整合

## 評論模型設計

評論系統使用自定義的 Comment 模型儲存用戶評論：

```python
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
```

## 評論表單設計

使用 Django ModelForm 為評論創建表單：


## URL 配置

評論功能的 URL 配置如下：

```python
urlpatterns = [
    # 原有路徑
    path('', views.home, name='home'),
    
    # 評論相關路徑
    path('comments/', views.comments, name='comments'),
    path('post_comment/', views.post_comment, name='post_comment'),
    path('delete_comment/<uuid:comment_id>/<str:del_pass>/', views.delete_comment, name='delete_comment'),
]
```

## 模板標籤擴展

為了方便在模板中訪問字典數據，建立了自定義模板過濾器：

```python
# drink_shop/templatetags/comment_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """取得字典中的項目"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''
```

## 管理界面整合

在 Django 管理界面中註冊評論模型，方便管理員審核和管理評論：

```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """評論管理界面配置"""
    list_display = ('nickname', 'drink', 'rating', 'message', 'enabled', 'pub_time')
    list_filter = ('drink', 'rating', 'enabled', 'pub_time')
    search_fields = ('nickname', 'message')
    date_hierarchy = 'pub_time'
    list_editable = ('enabled',)  # 允許直接在列表中編輯啟用狀態
```

## 用戶界面設計

評論區的用戶界面採用了響應式設計，確保在不同設備上有良好的顯示效果。主要包括評論表單和評論列表兩部分：

1. **評論表單**：使用者可以選擇飲品、評分，並填寫評論內容和刪除密碼
2. **評論列表**：以卡片形式展示評論，包括飲品圖片、評論者、評分、時間和內容

## 與會員系統的整合

評論功能與 JWT 會員系統無縫整合：

1. 會員發表的評論會自動獲准顯示，無需審核
2. 評論會自動關聯到會員帳號
3. 會員可以在會員中心查看自己的評論歷史

## 安全措施

評論系統實施了多項安全措施：

1. CSRF 保護防止跨站請求偽造
2. 表單數據驗證確保數據完整性
3. 刪除密碼機制保護用戶評論
4. 評論審核機制防止不適當內容

## 未來擴展計劃

未來可能的功能擴展包括：

1. 評論回覆功能，讓管理員可以回覆用戶評論
2. 評論點讚功能，讓用戶可以對有用的評論表示讚賞
3. 評論排序和過濾功能，方便用戶查找特定評論
4. 評論圖片上傳功能，讓用戶可以分享自己的飲品照片
5. 情感分析功能，自動分析評論情感傾向

## 結論

茶香飲品評論區功能為網站增添了互動性和用戶參與度，讓顧客可以分享自己的體驗和意見。這不僅有助於建立社區感，也為企業提供了寶貴的顧客反饋，幫助不斷提升產品和服務質量。通過與會員系統的整合，評論功能進一步鼓勵用戶註冊成為會員，促進用戶忠誠度和參與度。

# 智能客服功能介紹

## 概述

本次實作的智能客服是一個懸浮於網頁右下角的聊天視窗，使用 Google Gemini 大型語言模型 (LLM) 提供即時、自然的對話體驗。此功能讓用戶能夠詢問飲料店相關問題，獲得專業且個性化的回答。

## 技術架構

### 前端架構
- 使用原生 JavaScript 與 Socket.IO 客戶端
- 懸浮式聊天視窗 CSS 設計
- 即時打字效果模擬真人回覆感

### 後端架構
- Django 網頁框架作為主要服務
- Socket.IO 伺服器處理即時通訊
- Google Gemini API 處理自然語言理解與生成

### 通訊流程
- 用戶訊息透過 Socket.IO 發送至伺服器
- 伺服器轉發至 Gemini API 處理
- 回應以逐字流式傳輸回前端

## 關鍵功能

1. **即時對話**：透過 Socket.IO 實現無需頁面重載的即時通訊
2. **自然語言處理**：使用 Gemini 模型理解用戶意圖並生成自然回應
3. **店鋪知識整合**：整合飲料店菜單、價格、優惠等資訊
4. **打字效果**：實現逐字顯示的打字效果，增強使用者體驗
5. **響應式設計**：在各種設備上皆能良好顯示與操作

## 技術實現方式

智能客服功能透過以下幾個關鍵技術組件實現：

1. **Socket.IO 通訊**：建立即時雙向通訊通道
2. **Gemini API**：處理自然語言理解與回應生成
3. **逐字輸出機制**：實現打字效果增強用戶體驗
4. **知識庫整合**：提供飲料店專業知識支援
5. **懸浮式界面**：不干擾主要網頁內容的交互設計

## 客製化飲料店知識

智能客服整合了飲料店的專業知識，包括：
- 完整菜單與價格
- 店家資訊（地址、電話、營業時間）
- 特殊優惠與活動
- 常見問題解答

實作方式：將飲料店資訊整理成結構化文本，作為模型的上下文提示。

```python
tea_shop_knowledge = """
茶香飲品是一家專門提供高品質手搖飲料的店。以下是我們的主要信息：

店名：茶香飲品
地址：台北市信義區信義路五段100號
營業時間：週一至週日 10:00-22:00
電話：02-1234-5678
Email：info@chaxiang.com

主要產品類別：
1. 人氣茶飲：包括珍珠奶茶(60元)、芒果綠茶(75元)、鮮奶茶(65元)
2. 特調飲品：包括繽紛水果茶(85元)、抹茶拿鐵(80元)、檸檬冬瓜茶(70元)

杯型選擇：
- 中杯（基本價格）
- 大杯（+10元）

配料選擇：珍珠、布丁、仙草、茶凍
"""
```

## 用戶體驗設計

1. **直覺式操作**：懸浮按鈕易於發現，點擊即可開啟對話
2. **自然對話流**：模型經過提示優化，回應更加自然友善
3. **視覺反饋**：打字動畫提供視覺反饋，增加互動感
4. **品牌一致性**：聊天界面採用與網站一致的視覺風格（#DFFFDF）
5. **預設歡迎訊息**：開啟對話即顯示友善的歡迎訊息

## 視覺設計

聊天視窗的視覺設計符合品牌風格，使用清新的綠色 (#DFFFDF) 作為主色調，搭配簡潔的界面元素，讓用戶能夠直觀地進行交流。界面包含圓形聊天圖標、彈出式對話框、訊息氣泡以及輸入區域，整體設計注重易用性和視覺舒適度。

## 實際應用

該智能客服可以：
- 回答關於菜單、價格的詢問
- 提供店家資訊和營業時間
- 解釋飲品成分和特色
- 介紹當前促銷活動
- 協助解決常見問題

## 執行方法

1. **安裝所需套件**：
```bash
pip install django djangorestframework google-generativeai python-socketio eventlet
```

2. **取得 Google Gemini API 金鑰**：
   - 訪問 Google AI Studio (https://aistudio.google.com/)
   - 在設定頁面中創建 API 金鑰
   - 將金鑰添加到 socketio_server.py 文件中

3. **啟動服務**：
```bash
# 啟動 Socket.IO 服務
python socketio_server.py

# 另一個終端，啟動 Django 服務
python manage.py runserver
```

## 未來改進方向

1. **對話歷史記錄**：實現對話歷史儲存功能
2. **多語言支援**：增加英文等其他語言支援
3. **訂單整合**：直接在對話中查詢或建立訂單
4. **顧客識別**：對會員提供個性化服務
5. **分析功能**：追蹤常見問題以優化服務

這個智能客服功能不僅提升了網站的互動性，也為顧客提供了即時、專業的服務體驗，代表了飲料店擁抱數位創新的決心。

# JWT 會員系統功能介紹

## 概述

本次實作的 JWT 會員系統是一個完整的會員管理解決方案，使用 JSON Web Token (JWT) 技術實現無狀態身份驗證。此功能讓用戶能夠註冊帳號、登入系統、查看個人資料，享受會員專屬功能，提供安全且現代化的用戶體驗。


## 技術架構

### 前端架構
- 使用原生 JavaScript 處理用戶交互
- HTML 表單與 CSS 樣式設計
- localStorage 存儲與管理 JWT 令牌
- Fetch API 進行非同步請求

### 後端架構
- Django 網頁框架作為主要服務
- Django REST framework 提供 API 端點
- djangorestframework-simplejwt 處理 JWT 身份驗證
- SQLite 資料庫儲存會員資料

### 認證流程
- 用戶註冊或登入以獲取 JWT 令牌
- 前端儲存 access token 和 refresh token
- 後續請求中附加 access token 進行身份驗證
- access token 過期後使用 refresh token 獲取新的 access token

## 關鍵功能

1. **會員註冊**：用戶可創建個人帳號，提供用戶名、電子郵件、手機號碼和密碼
2. **會員登入**：使用用戶名和密碼登入，獲取 JWT 令牌
3. **會員中心**：查看個人資料、會員等級和積分
4. **訂單關聯**：將訂單與會員帳號自動關聯
5. **會員等級**：基於積分的會員等級系統（銅卡、銀卡、金卡）
6. **安全認證**：使用 JWT 令牌實現無狀態、安全的身份驗證
7. **令牌刷新**：使用 refresh token 自動更新過期的 access token

## 技術實現方式

JWT 會員系統透過以下幾個關鍵技術組件實現：

1. **Django REST framework**：提供 API 框架支持
2. **Simple JWT**：處理 JWT 令牌的生成、驗證和刷新
3. **會員模型設計**：擴展 Django 內建用戶模型
4. **前端 Token 管理**：使用 localStorage 安全儲存令牌
5. **RESTful API 設計**：清晰的 API 端點結構
6. **安全認證流程**：完整的登入、令牌驗證與刷新流程

## 會員模型設計

會員系統使用自定義模型擴展 Django 內建的用戶模型


## 組員分工情況 (共100%)

| 組員     | 貢獻比例 | 負責內容                     |
|----------|----------|------------------------------|
| 蔡承燁   | 33.3%      | 茶香飲品評論區功能介紹          |
| 章程睿   | 33.3%      | 智能客服功能介紹        |
| 陳皓偉   | 33.3%      | JWT 會員系統功能介紹    |
