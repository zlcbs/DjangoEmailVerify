from django import forms
from django.core.exceptions import ValidationError

from user.models import Users


# 定义验证器
def nickname_validate(nickname):
    u = Users.objects.filter(nickname=nickname)
    if len(u):
        print(len(u))
        raise ValidationError('用户名已存在')


# 定义表单
class RegisterForm(forms.Form):
    nickname = forms.CharField(validators=[nickname_validate],
                               label='用户名',
                               max_length=16,
                               min_length=4,
                               required=True,
                               widget=forms.TextInput(),
                               )

    password = forms.CharField(label='密码',
                               max_length=64,
                               min_length=6,
                               required=True,
                               widget=forms.PasswordInput())

    email = forms.EmailField(label='邮箱',
                             max_length=32,
                             required=True)

    age = forms.CharField(label='年龄',
                          max_length=3,
                          required=False)

    sex = forms.ChoiceField(label='性别',
                            choices=((0, '男'), (1, '女'),),
                            required=False)
