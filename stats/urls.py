from django.views.generic import RedirectView
from django.urls import path


app_name = 'stats'
urlpatterns = [
    path('', RedirectView.as_view(url='https://ddd.raylu.net'), name='index')
]
