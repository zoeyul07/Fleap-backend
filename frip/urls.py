from django.urls import path

from .views import DetailView, DailyView, MainView

urlpatterns = [
    path('/<int:products_id>', DetailView.as_view()),
    path('/daily',DailyView.as_view()),
    path('', MainView.as_view()),
]
