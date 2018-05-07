from django.apps import apps
from django.test.runner import DiscoverRunner


class ManagedModelTestRunner(DiscoverRunner):
    """
    Automatically makes all unmanaged models from statbot
    managed for the duration of the test run, so that Django
    creates the statbot tables for us to use during testing.
    """

    def setup_test_environment(self, **kwargs):
        self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super().setup_test_environment(**kwargs)

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment(**kwargs)
        for m in self.unmanaged_models:
            m._meta.managed = False
