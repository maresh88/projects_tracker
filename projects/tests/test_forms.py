from profiles.tests.test_models import LoggedUser
from projects.forms import CommentForm


class TestCommentForm(LoggedUser):
    def test_comment_form_body_field_has_no_label(self):
        form = CommentForm(data={
            'body': 'test'
        })
        self.assertFalse(form.fields['body'].label)
