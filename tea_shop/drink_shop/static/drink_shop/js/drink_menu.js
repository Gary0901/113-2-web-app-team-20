// 等待文檔加載完成
document.addEventListener('DOMContentLoaded', function() {
    // 獲取所有飲料項目
    const drinkItems = document.querySelectorAll('.drink-item');
    
    // 為每個飲料項目添加事件監聽器
    drinkItems.forEach(function(item) {
        // 獲取每個項目中的圖片和覆蓋層
        const img = item.querySelector('img');
        const overlay = item.querySelector('.drink-overlay');
        
        // 鼠標移入事件
        item.addEventListener('mouseover', function() {
            // 圖片變暗並放大
            img.style.filter = 'brightness(50%)';
            img.style.transform = 'scale(1.05)';
            
            // 顯示覆蓋層
            overlay.style.opacity = '1';
        });
        
        // 鼠標移出事件
        item.addEventListener('mouseout', function() {
            // 恢復圖片原狀
            img.style.filter = 'brightness(100%)';
            img.style.transform = 'scale(1)';
            
            // 隱藏覆蓋層
            overlay.style.opacity = '0';
        });
    });
});