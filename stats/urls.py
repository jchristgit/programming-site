from django.urls import path
from django.views.generic import RedirectView


app_name = "stats"
urlpatterns = [
    path("", RedirectView.as_view(url="https://ddd.raylu.net"), name="index")
]
