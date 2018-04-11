from django.contrib.auth.models import User
from django.views import generic



class ProfileView(generic.DetailView):
    model = User
