# Generated by Django 3.1.7 on 2021-08-05 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game_age_min', models.IntegerField()),
                ('game_age_max', models.IntegerField()),
                ('game_contains_mature_content', models.BooleanField()),
                ('game_description_de', models.TextField()),
                ('game_description_en', models.TextField()),
                ('game_description_es', models.TextField()),
                ('game_description_fr', models.TextField()),
                ('game_description_pt', models.TextField()),
                ('game_image_path', models.CharField(max_length=100)),
                ('game_name', models.CharField(max_length=80)),
                ('game_number_in_stock', models.IntegerField()),
                ('game_number_times_consulted', models.IntegerField()),
                ('game_number_times_borrowed', models.IntegerField()),
                ('game_player_number_min', models.IntegerField()),
                ('game_player_number_max', models.IntegerField()),
                ('game_type', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_birth_date', models.DateField()),
                ('user_email_adress', models.CharField(max_length=50)),
                ('user_login', models.CharField(max_length=30)),
                ('user_password', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('borrowing_deadline', models.DateTimeField()),
                ('borrowing_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.game')),
                ('borrowing_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
