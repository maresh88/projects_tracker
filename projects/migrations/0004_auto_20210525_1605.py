# Generated by Django 3.2.3 on 2021-05-25 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_comment_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
