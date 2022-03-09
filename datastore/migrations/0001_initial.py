# Generated by Django 4.0.3 on 2022-03-08 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text="Manager's First Name", max_length=30)),
                ('last_name', models.CharField(help_text="Manager's Last Name", max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Company Name', max_length=200)),
                ('description', models.TextField(help_text='Company Description')),
                ('address', models.TextField(help_text='Company Address')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datastore.manager')),
            ],
        ),
    ]