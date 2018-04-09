from django.contrib.auth.models import User

# Create your views here.
from django.views import generic


class ProfileView(generic.DetailView):
    model = User
