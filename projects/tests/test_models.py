from test_plus.test import TestCase

from projects.models import Project, Comment


class DummyProjectsModels(TestCase):
    def setUp(self):
        self.author = self.make_user('test')
        self.project = Project.objects.create(
            author=self.author,
            title='test 1',
        )


class TestProjectModel(DummyProjectsModels):

    def test_project_model_creation(self):
        self.assertEqual(self.project.slug, '1-test-1')
        self.assertEqual(str(self.project), 'test 1')

    def test_project_absolute_url(self):
        self.assertEqual(self.project.get_absolute_url(), '/projects/1/1-test-1/')


class TestCommentModel(DummyProjectsModels):

    def test_comment_model_creation(self):
        comment = Comment.objects.create(
            project=self.project,
            author=self.author,
            body='test body'
        )
        self.assertEqual('comment "test body" by test', str(comment))