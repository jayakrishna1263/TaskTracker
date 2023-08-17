# Generated by Django 4.2.4 on 2023-08-17 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_taskassignments_taskassignment_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taskassignment',
            unique_together={('task_id', 'member_id')},
        ),
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together={('member_id', 'team_id')},
        ),
    ]