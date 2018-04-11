from django.urls import path

from .views import ProfileView, NickRedirectView


app_name = 'profiles'
urlpatterns = [
    path('~<str:nick>', NickRedirectView.as_view(), name='nick_redirect'),
    path('<int:pk>', ProfileView.as_view(), name='detail')
]
