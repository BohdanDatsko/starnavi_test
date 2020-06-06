# Generated by Django 3.0.7 on 2020-06-06 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.TextField()),
                ('like', models.BigIntegerField(default=0)),
                ('unlike', models.BigIntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='CommentLikeUnlike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('unlike', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'CommentLikeUnlike',
                'verbose_name_plural': 'CommentLikeUnlikes',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('content', models.TextField()),
                ('like', models.BigIntegerField(default=0)),
                ('unlike', models.BigIntegerField(default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='PostLikeUnlike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('unlike', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'PostLikeUnlike',
                'verbose_name_plural': 'PostLikeUnlikes',
            },
        ),
    ]