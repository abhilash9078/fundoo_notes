from django.urls import path
from user.views import UserLoginView, UserRegistrationView, UserProfileView, UserChangePasswordView,\
    UserForgotPasswordResetView, SendForgotPasswordResetEmailView,UserProfileVerificationView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify_account/<uid>/', UserProfileVerificationView.as_view(), name='verification'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('forgot_password/send_email/', SendForgotPasswordResetEmailView.as_view(), name='forgot_password_send_email'),
    path('reset_password/<uid>/<token>/', UserForgotPasswordResetView.as_view(), name='forgot_password'),

]
