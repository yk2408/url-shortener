from django.urls import path

from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("shorten", URLShortener.as_view(), name="shorten"),
    path("<str:short_url>", RedirectURLView.as_view(), name="redirect"),
    path('error/', ErrorView.as_view(), name='error'),
    path('delete_url/<str:short_url>', DeleteURL.as_view(), name='delete'),


]