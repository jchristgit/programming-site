from django.urls import path

from . import views
from .feeds import LatestGuidesAtomFeed, LatestGuidesRSSFeed


app_name = 'guides'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create', views.CreateView.as_view(), name='create'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.EditView.as_view(), name='edit'),
    path('<int:pk>/delete', views.DeleteView.as_view(), name='delete'),
    path('feed/atom', LatestGuidesAtomFeed(), name='feed_atom'),
    path('feed/rss', LatestGuidesRSSFeed(), name='feed_rss')
]
