document.addEventListener('DOMContentLoaded', () => {
    // 選擇元素
    const chatIcon = document.getElementById('chat-icon');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    
    // 建立Socket.IO連接
    const socket = io('http://localhost:8001');
    
    // 連接事件處理
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    // 打開聊天視窗
    chatIcon.addEventListener('click', () => {
        chatWindow.classList.add('active');
        scrollToBottom();
    });
    
    // 關閉聊天視窗
    closeChat.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });
    
    // 發送消息
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            // 添加用戶消息
            addMessage(message, 'user-message');
            
            // 顯示打字指示器
            typingIndicator.style.display = 'block';
            
            // 發送到服務器
            socket.emit('chat_request', { message });
            
            // 清空輸入框
            messageInput.value = '';
        }
    }
    
    // 發送按鈕點擊事件
    sendButton.addEventListener('click', sendMessage);
    
    // 輸入框按Enter發送
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // 接收逐字回應
    let currentResponseDiv = null;
    
    socket.on('chat_response_chunk', (data) => {
        if (!currentResponseDiv) {
            // 創建新的回應div
            currentResponseDiv = document.createElement('div');
            currentResponseDiv.className = 'message bot-message';
            currentResponseDiv.textContent = '';
            
            // 在打字指示器前插入
            chatMessages.insertBefore(currentResponseDiv, typingIndicator);
        }
        
        // 添加文字
        currentResponseDiv.textContent += data.text;
        scrollToBottom();
    });
    
    // 接收完成信號
    socket.on('chat_response_complete', () => {
        // 隱藏打字指示器
        typingIndicator.style.display = 'none';
        currentResponseDiv = null;
        scrollToBottom();
    });
    
    // 添加消息到聊天區域
    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        messageDiv.textContent = text;
        chatMessages.insertBefore(messageDiv, typingIndicator);
        scrollToBottom();
    }
    
    // 滾動到底部
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});