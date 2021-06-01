from profiles.tests.test_models import LoggedUser

from ..models import Project, Comment


class ProjectsViews(LoggedUser):
    def setUp(self):
        super(ProjectsViews, self).setUp()
        self.project = Project.objects.create(
            author=self.manager,
            title='test 1',
        )

    def test_project_list_GET(self):
        response = self.get_check_200('projects:projects')
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_detail_GET(self):
        url = self.reverse('projects:detail', pk=1, slug='1-test-1')
        response = self.get_check_200(url)
        self.assertTemplateUsed(response, 'projects/project_detail.html')

    def test_project_update(self):
        url = self.reverse('projects:update', pk=1, slug='1-test-1')
        response = self.post(url, data={
            'description': 'new description'
        })
        self.assertTemplateUsed(response, 'projects/project_create_update.html')

    def test_project_create_GET(self):
        response = self.get_check_200('projects:create')
        self.assertTemplateUsed(response, 'projects/project_create_update.html')

    def test_project_create_POST(self):
        response = self.post('projects:create', data={
            'author': self.manager,
            'title': 'test creation',
            'description': 'description',
            'project_status': 's'
        })
        self.assertRedirects(response, '/projects/2/1-test-creation/')

    def test_project_detail_leave_comment_POST(self):
        url = self.reverse('projects:detail', pk=1, slug='1-test-1')
        response = self.post(url, data={
            'project': self.project,
            'author': self.manager,
            'body': 'test body'
        })
        self.assertRedirects(response, url)

    def test_filter_view(self):
        response = self.get_check_200('projects:filter')
        self.assertTemplateUsed(response, 'projects/project_list.html')
