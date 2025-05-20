from django import forms
from .models import Comment
from captcha.fields import CaptchaField

class CommentForm(forms.ModelForm):
    captcha = CaptchaField(label='驗證碼')
    
    class Meta:
        model = Comment
        fields = ['nickname', 'drink', 'rating', 'message', 'del_pass']
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['nickname'].label = '你的暱稱'
        self.fields['drink'].label = '評論飲品'
        self.fields['rating'].label = '評分'
        self.fields['message'].label = '評論內容'
        self.fields['del_pass'].label = '刪除密碼'
        
        # 添加樣式
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })