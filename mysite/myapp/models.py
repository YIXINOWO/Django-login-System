from django.db import models

class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)  # 增加长度以存储加密后的密码
    age = models.IntegerField()
    email = models.EmailField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_info'
