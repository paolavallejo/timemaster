# Generated by Django 4.2 on 2023-05-03 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('horario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=80)),
                ('fixed', models.BooleanField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='actividad_no_fija',
            name='usuario_id',
        ),
        migrations.RemoveField(
            model_name='horario_sueno',
            name='usuario_id',
        ),
        migrations.DeleteModel(
            name='Actividad_fija',
        ),
        migrations.DeleteModel(
            name='Actividad_no_fija',
        ),
        migrations.DeleteModel(
            name='Horario_sueno',
        ),
    ]
