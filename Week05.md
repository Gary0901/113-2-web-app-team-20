# Week05 作業報告 - Team 20

## 1️⃣ 練習了哪些當週上課的主題

### 🔹 JavaScript 表單驗證
- 熟悉 `form` 元素基本結構與 `onsubmit` 事件觸發時機
- 使用 JavaScript 驗證文字欄位是否為空、電話格式是否正確
- 驗證使用者是否選擇了必要的選項（如杯型、飲品種類）
- 使用 `return false` 阻止錯誤表單送出
- 利用 DOM 動態產生訂單摘要內容，展示使用者輸入的資料

### 🔹 DOM 操作與事件處理
- 透過 `document.createElement()` 動態新增 HTML 元素
- 使用 `addEventListener()` 監聽 `mouseover`、`mouseout` 等事件
- 實作滑鼠懸停時菜單圖片變暗、放大等效果
- 將 JavaScript 程式碼獨立成檔案以提升可維護性

---

## 2️⃣ 額外找了與當週上課的主題相關的程式技術

### ✅ 倒數計時與排程功能
- 使用 `new Date()` 處理時間資訊，計算與活動開始的倒數天數
- 透過 `setInterval()` 每秒更新倒數資訊，並以 `clearInterval()` 停止排程
- 顯示活動倒數計時，並在活動開始後自動顯示訊息更新

### ✅ 輪播圖實作
- 使用陣列儲存圖片與標題，搭配 `setInterval()` 實作自動輪播
- 加入淡入淡出效果增強視覺吸引力
- 圖片輪播與倒數功能皆支援不同螢幕尺寸，實現響應式設計

### ✅ 模態框與互動流程優化
- 實作訂單送出前的彈跳視窗 (modal)，提示使用者確認
- 利用 `position: fixed` 與 `z-index` 設計覆蓋層與視窗樣式
- 結合 JavaScript 控制模態框開關邏輯，提升互動性

### ❗ 關於 React 的使用說明
本週老師有提及使用 React 進行實作，但我們組在討論後認為，團隊成員目前對 React 還不夠熟悉，因此決定先專注在練習 **原生 JavaScript 的 DOM 操作與事件處理**，以強化對基本前端邏輯與結構的掌握。

我們希望先打好基礎，未來再進一步使用 React 重構功能時，能有更清楚的對照與理解。目前所有互動功能（如表單驗證、倒數計時、圖片輪播與模態框）皆以原生 JavaScript 實作完成，並已成功整合至專案中。

---

## 3️⃣ 組員分工情況 (共100%)

| 組員     | 貢獻比例 | 負責內容                     |
|----------|----------|------------------------------|
| 蔡承燁   | 33.3%      | CSS 設計與互動樣式調整          |
| 章程睿   | 33.3%      | HTML 設計與結構建立        |
| 陳皓偉   | 33.3%      | JavaScript 功能整合與樣式修正    |
