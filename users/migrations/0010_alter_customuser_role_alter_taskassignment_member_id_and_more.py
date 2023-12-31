# Generated by Django 4.2.4 on 2023-08-17 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Team leader', 'Team leader'), ('Team memeber', 'Team memeber')], default='Manager', max_length=100),
        ),
        migrations.AlterField(
            model_name='taskassignment',
            name='member_id',
            field=models.ForeignKey(limit_choices_to={'role': 'Team memeber'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_lead',
            field=models.ForeignKey(limit_choices_to={'role': 'Team leader'}, on_delete=django.db.models.deletion.CASCADE, related_name='team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='member_id',
            field=models.ForeignKey(limit_choices_to={'role': 'Team memeber'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
