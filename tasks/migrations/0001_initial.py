from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labels', '0001_initial'),
        ('statuses', '0002_alter_status_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='authored_tasks',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'executor',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='assigned_tasks',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ('labels', models.ManyToManyField(blank=True, to='labels.label')),
                (
                    'status',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='tasks',
                        to='statuses.status',
                    ),
                ),
            ],
        ),
    ]
