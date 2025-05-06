# Week08 作業報告 - Django Template 實作

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

## 截圖

（可以在這裡添加首頁、訂單狀態頁的截圖）

## 下週計畫

- 學習 Custom Template Tags 和 Filters
- 實作更複雜的表單驗證
- 加入用戶認證功能
