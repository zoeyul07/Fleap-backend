from django.urls import path
from .views import SignUpView, SignInView, KakaoView, LikeView

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/kakao', KakaoView.as_view()),
    path('/like', LikeView.as_view()),
]
