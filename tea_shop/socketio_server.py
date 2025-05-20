# socketio_server.py 修改版本

import socketio
import google.generativeai as genai
import os

# 設置Google Gemini API金鑰
GEMINI_API_KEY = 'AIzaSyA3oDJBDyd1tgINE89XPR52Rk9YwEJk2ww'  # 請替換為您的實際API金鑰

# 初始化Socket.IO伺服器
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

# 配置Gemini
genai.configure(api_key=GEMINI_API_KEY)

# 定義茶香飲品店的知識庫
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

特色與優勢：
- 使用新鮮水果和優質茶葉
- 天然配料，不添加人工色素
- 可客製化甜度和冰量
- 提供外送服務（透過電話訂購）

活動信息：
- 周年慶將於2025年6月15日舉行
- 買二送一促銷活動每週三進行

常見問題：
- 訂單一般10-15分鐘內完成
- 可以提前一天預訂大量訂單
- 會員可享有點數累積和生日優惠
"""

# 創建模型配置
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "response_mime_type": "text/plain",
    "max_output_tokens": 4096,
}

# 創建安全設置
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# 初始化模型
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    generation_config=generation_config,
    safety_settings=safety_settings
)

@sio.event
def connect(sid, environ):
    print(f"客戶端連接: {sid}")

@sio.event
def disconnect(sid):
    print(f"客戶端斷開: {sid}")

@sio.event
def chat_request(sid, data):
    user_message = data.get('message', '')
    
    try:
        # 構建完整的對話請求（包含系統指令）
        prompt = f"""你是「茶香飲品」的AI智能客服。請使用以下知識來回答有關茶香飲品的問題：

{tea_shop_knowledge}

當談到我們的飲品時，請熱情推薦我們的特色產品。如果詢問的問題不在你的知識範圍內，
請禮貌地說明你無法提供該信息，並建議客戶直接致電或到店詢問。
請使用親切、友善且專業的語氣回答。盡量簡短、清晰地回答。

用戶問題: {user_message}
"""

        # 生成回應，使用流式輸出
        response = model.generate_content(prompt, stream=True)
        
        # 逐字發送回應
        for chunk in response:
            if hasattr(chunk, 'text'):
                # 每個文字塊可能還是較大，進一步分割成單個字元
                text_chunk = chunk.text
                for char in text_chunk:
                    sio.emit('chat_response_chunk', {'text': char}, room=sid)
                    # 可以添加小延遲使顯示更自然
                    # import time
                    # time.sleep(0.01)
        
        # 發送完成信號
        sio.emit('chat_response_complete', room=sid)
    except Exception as e:
        print(f"Error generating response: {e}")
        sio.emit('chat_response_chunk', {'text': f"抱歉，我暫時無法回答您的問題。請稍後再試。錯誤: {str(e)}"}, room=sid)
        sio.emit('chat_response_complete', room=sid)

# 直接執行時運行伺服器
if __name__ == '__main__':
    import eventlet
    port = 8001
    print(f"Starting Socket.IO server on port {port}...")
    eventlet.wsgi.server(eventlet.listen(('', port)), app)