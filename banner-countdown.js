// Banner 輪播功能
let currentBannerIndex = 0;
const bannerImages = [
    "./picture/drink1.jpg", // 第一張輪播圖片 (實際使用時請替換成真實圖片路徑)
    "./picture/drink2.jpg", // 第二張輪播圖片
    "./picture/drink3.jpg"  // 第三張輪播圖片
];
const bannerTitles = [
    "春季新品上市", 
    "夏季特惠活動",
    "周年慶即將到來"
];

// 每隔 5 秒切換圖片
function rotateBanner() {
    currentBannerIndex = (currentBannerIndex + 1) % bannerImages.length;
    document.getElementById('banner-image').src = bannerImages[currentBannerIndex];
    document.getElementById('banner-title').textContent = bannerTitles[currentBannerIndex];
}

// 設定 Banner 輪播間隔時間（每 5 秒切換一次）
const bannerInterval = setInterval(rotateBanner, 5000);

// 倒數計時功能
function updateCountdown() {
    // 設定周年慶日期（這裡假設是 2025 年 4 月 15 日）
    const anniversaryDate = new Date("2025-04-15T00:00:00");
    
    // 取得當前時間
    const now = new Date();
    
    // 計算剩餘時間（毫秒）
    const diff = anniversaryDate - now;
    
    // 如果活動已經開始，顯示活動進行中
    if (diff <= 0) {
        document.getElementById('countdown-days').textContent = "0";
        document.getElementById('countdown-hours').textContent = "0";
        document.getElementById('countdown-minutes').textContent = "0";
        document.getElementById('countdown-seconds').textContent = "0";
        document.getElementById('countdown-message').textContent = "周年慶活動進行中！";
        clearInterval(countdownInterval); // 停止倒數
        return;
    }
    
    // 計算剩餘的天、小時、分鐘和秒數
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    
    // 更新 HTML 元素
    document.getElementById('countdown-days').textContent = days;
    document.getElementById('countdown-hours').textContent = hours;
    document.getElementById('countdown-minutes').textContent = minutes;
    document.getElementById('countdown-seconds').textContent = seconds;
}

// 立即執行一次
updateCountdown();

// 每秒更新一次倒數計時
const countdownInterval = setInterval(updateCountdown, 1000);