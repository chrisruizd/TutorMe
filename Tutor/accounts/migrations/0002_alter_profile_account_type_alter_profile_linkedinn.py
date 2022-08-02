# Generated by Django 4.0.6 on 2022-07-29 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_Type',
            field=models.CharField(blank=True, choices=[('student', 'STUDENT'), ('tutor', 'TUTOR')], default='none', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linkedinn',
            field=models.CharField(default='none', max_length=200, null=True),
        ),
    ]