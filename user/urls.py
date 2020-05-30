from django.urls import path
from .views import SignUpView, SignInView, KakaoView, LikeView, InterestCategoryView, InterestFripView, MyFripView

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/kakao', KakaoView.as_view()),
    path('/like', LikeView.as_view()),
    path('/interestdetail',InterestCategoryView.as_view()),
    path('/interestfrip',InterestFripView.as_view()),
    path('/myfrip',MyFripView.as_view())
]
