
from django.urls import path
from techno import views

urlpatterns = [
    path("", views.HomeView.as_view()),
]
