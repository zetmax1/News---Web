from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/', dashboard, name='user_profile')
]