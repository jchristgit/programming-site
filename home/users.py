from django.contrib.auth.models import AnonymousUser


class CustomAnonymousUser(AnonymousUser):
    def __init__(self, _):
        super().__init__()
        self.is_member = False
