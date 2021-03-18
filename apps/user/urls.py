from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views
from .views import *

urlpatterns = [
    # for login page
    path('login/', views.LoginView.as_view(template_name='user/login.html'), name='login'),
    re_path(r'send-email/(?P<user_slug>[-\w]+)/', SendEmailVerification.as_view(), name='send-email'),
    path('activate/<uidb64>/<token>/', EmailVerify.as_view(), name='activate'),
    re_path(r'send-sms/(?P<user_slug>[-\w]+)/', SendSmsVerification.as_view(), name='send-sms'),
    re_path(r'mobile_verify/(?P<user_slug>[-\w]+)/', MobileVerify.as_view(), name='mobile_verify'),
    # this is for autocomplete field in home page header
    re_path(r'user_autocomplete/(?P<slug>[-\w]+)/', UserAutocomplete.as_view(), name='user_autocomplete'),
    re_path(r'search/(?P<slug>[-\w]+)/', FilterUser.as_view(), name='search_user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    re_path(r'edit_profile/(?P<slug>[-\w]+)/', UpdateUserProfile.as_view(), name='edit_profile'),
    # yet dont work on it
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
