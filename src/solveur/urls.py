from django.urls import path

from . import views

app_name = "solveur"
urlpatterns = [
    path("", views.index, name="index"),
    path("resolve/", views.resolve, name="resolve"),
]
