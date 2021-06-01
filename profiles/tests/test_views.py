from django.contrib.auth.models import User
from .test_models import LoggedUser


class TestProfileViews(LoggedUser):
    def test_search_reporter_is_ajax(self):
        xml_response = self.get(
            'profiles:search_reporter',
            extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(200, xml_response.status_code)

    def test_search_reporter_raise_bad_request_for_not_ajax(self):
        response = self.get('profiles:search_reporter')
        self.assertEqual(400, response.status_code)

    def test_search_reporter_not_found(self):
        xml_response = self.get(
            'profiles:search_reporter', data={'reporter': 'fake_reporter@mail.com'},
            extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
                   })
        self.assertEqual({'Not Ok': 'Not Found'}, xml_response.json())

