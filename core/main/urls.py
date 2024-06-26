from django.urls import path, include
from .views import search_dishes
urlpatterns = [
    path('', search_dishes)
]