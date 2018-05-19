from django.urls import path

from . import views


app_name = "profiles"
urlpatterns = [
    path("<int:pk>", views.ProfileDetailView.as_view(), name="detail"),
    path("<int:pk>/delete", views.ProfileDeleteView.as_view(), name="delete")
]
