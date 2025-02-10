from django.contrib import admin
from .models import UserInfo  # 假设你的模型名是UserInfo

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id'] + [field.name for field in UserInfo._meta.fields if field.name != 'id']
