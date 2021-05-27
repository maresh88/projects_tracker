from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):
    PROJECT_STATUS_CHOICE = (
        ('s', 'started'),
        ('p', 'in progress'),
        ('pp', 'postponed'),
        ('b', 'behind'),
        ('i', 'inactive'),
        ('c', 'closed'),
    )

    author = models.ForeignKey(User,
                               related_name='projects',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_year='created_at')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_status = models.CharField(max_length=2,
                                      choices=PROJECT_STATUS_CHOICE,
                                      default='s')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)
        index_together = ('id', 'slug')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.author_id}-{self.title}')
        super().save(*args, **kwargs)


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'comment \"{self.body}\" by {self.author}'
