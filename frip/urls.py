from django.urls import path

from .views import DetailView, DailyView, MainView, SearchView, PurchaseView, ReviewView

urlpatterns = [
    path('/<int:product_id>', DetailView.as_view()),
    path('/daily',DailyView.as_view()),
    path('', MainView.as_view()),
    path('/search', SearchView.as_view()),
    path('/<int:product_id>/purchase', PurchaseView.as_view()),
    path('/<int:product_id>/review', ReviewView.as_view())
]
