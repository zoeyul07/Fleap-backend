from django.urls import path

from .views import DetailView, DailyView

urlpatterns = [
    path('/<int:products_id>', DetailView.as_view()),
    path('/daily',DailyView.as_view()),
]
