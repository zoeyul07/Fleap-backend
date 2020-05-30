from django.urls    import path
from .views         import DailyView

urlpatterns = [
    path('/daily',DailyView.as_view()),
]
