# Generated by Django 3.0.4 on 2020-04-21 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200421_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity',
            field=models.CharField(choices=[('like', 'Like'), ('unlike', 'Unlike'), ('login', 'Login'), ('post', 'Post')], max_length=50),
        ),
    ]