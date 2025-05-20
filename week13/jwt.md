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

