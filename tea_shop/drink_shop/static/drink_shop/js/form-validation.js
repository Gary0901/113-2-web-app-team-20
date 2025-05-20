// 等待文檔加載完成
document.addEventListener('DOMContentLoaded', function() {
    // 獲取訂單表單
    const orderForm = document.getElementById('orderForm');
    
    // 加入表單提交事件監聽器
    if (orderForm) {
        orderForm.addEventListener('submit', function(event) {
            // 阻止表單默認提交行為
            event.preventDefault();
            
            // 驗證表單
            if (validateOrderForm(this)) {
                // 顯示訂單摘要
                showOrderSummary(this);
            }
        });
    }
});

// 表單驗證函式
function validateOrderForm(form) {
    // 檢查姓名是否為空
    if (form.name.value.trim() === "") {
        alert("請輸入您的姓名！");
        form.name.focus();
        return false;
    }

    // 檢查電話是否為空
    if (form.phone.value.trim() === "") {
        alert("請輸入您的電話！");
        form.phone.focus();
        return false;
    }

    // 檢查電話格式是否正確（台灣手機號碼格式）
    const phonePattern = /^(09)[0-9]{8}$/;
    if (!phonePattern.test(form.phone.value.trim())) {
        alert("請輸入有效的台灣手機號碼（例如：0912345678）！");
        form.phone.focus();
        return false;
    }

    // 檢查是否選擇杯型
    let cupSizeSelected = false;
    for (let i = 0; i < form.size.length; i++) {
        if (form.size[i].checked) {
            cupSizeSelected = true;
            break;
        }
    }

    if (!cupSizeSelected) {
        alert("請選擇杯型（中杯/大杯）！");
        return false;
    }
    
    return true;
}

// 顯示訂單摘要
function showOrderSummary(form) {
    // 獲取選擇的飲品
    const drinkSelect = form.drink;
    const selectedDrink = drinkSelect.options[drinkSelect.selectedIndex].text;
    
    // 獲取選擇的杯型
    let selectedSize = "";
    for (let i = 0; i < form.size.length; i++) {
        if (form.size[i].checked) {
            selectedSize = form.size[i].nextElementSibling.textContent;
            break;
        }
    }
    
    // 獲取選擇的配料
    let selectedToppings = [];
    for (let i = 0; i < form.toppings.length; i++) {
        if (form.toppings[i].checked) {
            selectedToppings.push(form.toppings[i].nextElementSibling.textContent);
        }
    }
    
    // 準備訂單摘要
    let summaryHTML = `
        <div class="order-summary">
            <h3>您的訂單摘要</h3>
            <p><strong>姓名：</strong>${form.name.value}</p>
            <p><strong>電話：</strong>${form.phone.value}</p>
            <p><strong>飲品：</strong>${selectedDrink}</p>
            <p><strong>杯型：</strong>${selectedSize}</p>
            <p><strong>配料：</strong>${selectedToppings.length > 0 ? selectedToppings.join('、') : '無'}</p>
            <p><strong>備註：</strong>${form.notes.value.trim() || '無'}</p>
            <div class="summary-actions">
                <button onclick="submitOrder()">確認訂單</button>
                <button onclick="cancelOrder()">修改訂單</button>
            </div>
        </div>
    `;
    
    // 創建摘要元素
    const summaryContainer = document.createElement('div');
    summaryContainer.id = 'orderSummaryContainer';
    summaryContainer.className = 'summary-container';
    summaryContainer.innerHTML = summaryHTML;
    
    // 添加遮罩背景
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    overlay.id = 'summaryOverlay';
    
    // 添加到頁面
    document.body.appendChild(overlay);
    document.body.appendChild(summaryContainer);
}

// 確認訂單
function submitOrder() {
    // 檢查是否有會員 token
    const accessToken = localStorage.getItem('access_token');
    
    // 原有的表單提交
    const form = document.getElementById('orderForm');
    
    // 如果已登入會員，添加 token 標頭
    if (accessToken) {
        // 使用 fetch API 提交表單
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            },
            body: formData
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('訂單提交過程中發生錯誤，請稍後再試。');
        });
    } else {
        // 非會員直接提交表單
        form.submit();
    }
    
    // 清除摘要和遮罩
    closeOrderSummary();
}

// 取消訂單
function cancelOrder() {
    closeOrderSummary();
}

// 關閉訂單摘要
function closeOrderSummary() {
    const summaryContainer = document.getElementById('orderSummaryContainer');
    const overlay = document.getElementById('summaryOverlay');
    
    if (summaryContainer) {
        document.body.removeChild(summaryContainer);
    }
    
    if (overlay) {
        document.body.removeChild(overlay);
    }
}