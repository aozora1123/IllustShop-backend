from django.urls import path
from .views import (RegisterAPIView,
LoginAPIView, 
LogoutAPIView
)

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='user-registration'),
    path('login', LoginAPIView.as_view(), name='user-login'),
    path('logout', LogoutAPIView.as_view(), name='user-logout'),

]