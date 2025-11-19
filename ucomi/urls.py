from django.urls import path
from commute import views  

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]

