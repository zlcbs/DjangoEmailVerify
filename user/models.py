from django.conf import settings
from django.db import models
# django密码转换
from django.contrib.auth.hashers import make_password
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from itsdangerous import BadSignature, SignatureExpired


# Create your models here.

class Users(models.Model):
    nickname = models.CharField(max_length=16, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=32, null=False, blank=False, unique=True)
    password = models.CharField(max_length=64, null=False, blank=False)
    head = models.ImageField(default="decault.png")
    age = models.CharField(max_length=3, blank=True, null=True)
    sex = models.CharField(max_length=2, blank=True, null=True)
    isactivate = models.BooleanField(default=False)

    def save(self):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()

    # 生成token
    def generate_activate_token(self, expires_in=360):
        s = Serializer(settings.SECRET_KEY, expires_in)
        return s.dumps({'id': self.id})

    # token校验
    @staticmethod
    def check_activate_token(token):
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except BadSignature:
            return '无效的激活码'
        except SignatureExpired:
            return '激活码已过期'
        user = Users.objects.filter(id=data.get('id'))[0]
        if not user:
            return '激活的账号不存在'
        if not user.isactivate:
            user.isactivate = True
            user.save()
        return '激活成功'
