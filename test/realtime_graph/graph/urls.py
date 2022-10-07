from django import views
from django.urls import URLPattern, path
from .views import index


urlpatterns = [
    path('', index)
] 