from django.http import HttpResponseForbidden


class MemberRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_member:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.object.author and not self.request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
