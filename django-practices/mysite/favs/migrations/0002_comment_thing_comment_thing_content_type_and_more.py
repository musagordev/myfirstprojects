# Generated by Django 4.0.7 on 2023-04-20 14:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('favs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(validators=[django.core.validators.MinLengthValidator(3, 'Comment must be greater than 3 characters')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='thing',
            name='comment',
            field=models.ManyToManyField(related_name='forum_comments', through='favs.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='thing',
            name='content_type',
            field=models.CharField(blank=True, help_text='The MIMEType of the file', max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='thing',
            name='picture',
            field=models.BinaryField(blank=True, editable=True, null=True),
        ),
        migrations.AddField(
            model_name='thing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='thing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thing_comment_id', to='favs.thing'),
        ),
    ]
