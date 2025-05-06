# drink_shop/context_processors.py
import datetime

def global_context(request):
    """為所有頁面提供全域變數"""
    now = datetime.datetime.now()
    is_open = (now.hour >= 10 and now.hour < 22)
    
    return {
        'is_open': is_open,
        'current_time': now,
    }