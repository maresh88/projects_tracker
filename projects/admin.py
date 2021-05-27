from django.contrib import admin


from .models import Comment, Project


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'slug',
                    'description', 'created_at', 'updated_at',
                    'project_status', 'is_active')
    prepopulated_fields = {"slug": ("author", "title")}
    list_filter = ('author', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-updated_at',)
    inlines = [CommentInline, ]
