from django.urls import path
from .views import SignUpView, SignInView, KakaoView

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/kakao', KakaoView.as_view()),
]
