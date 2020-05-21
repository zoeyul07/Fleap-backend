from django.urls import path

from .views import DetailView

urlpatterns = [
    path('/<int:products_id>', DetailView.as_view()),
]
