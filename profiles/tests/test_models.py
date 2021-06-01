from test_plus.test import TestCase
from django.contrib.auth.models import User

from profiles.models import Profile


class ProfileModelTest(TestCase):

    def test_binding_profile_and_user_after_creation(self):
        user = User.objects.create_user('name', 'test@test.com', 'pwd')
        self.assertEqual(str(user.profile), 'name')
        self.assertTrue(isinstance(user.profile, Profile))

    def test_parenting_for_profile_model(self):
        manager = User.objects.create_user('manager', 'test@test.com', 'pwd')
        reporter = User.objects.create_user('reporter', 'test@test.com', 'pwd')
        reporter.parent = manager.profile
        self.assertEqual(reporter.parent.user.username, 'manager')


class LoggedUser(TestCase):
    def setUp(self):
        self.manager = self.make_user('manager')
        self.reporter = self.make_user('reporter')
        self.reporter.email = 'reporter@mail.com'
        self.reporter.parent = self.manager.profile
        Profile.tree.rebuild()
        self.client.force_login(user=self.manager)
