from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutViewCustom.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', dashboard, name='user_profile'),
    path('signup/', user_register, name='register'),
    # path('profile/edit/', user_edit, name='user_edit'),
    path('profile/edit/', EditUserView.as_view(), name='profile_edit'),

]