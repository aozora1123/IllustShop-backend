from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Account  # 假設你的自訂User Model名為CustomUser

class AccountUserAdmin(UserAdmin):
    pass  # 在這裡可以自訂你想要的管理者介面設定

admin.site.register(Account, AccountUserAdmin)