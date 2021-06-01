from .test_models import LoggedUser
from profiles.forms import ReporterSearchForm


class TestSearchReporterForm(LoggedUser):
    def test_search_reporter_form_valid(self):
        form = ReporterSearchForm(data={
            'reporter': 'test@test.com'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['reporter'], 'test@test.com')
