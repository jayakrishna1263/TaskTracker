# Generated by Django 4.2.4 on 2023-08-17 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='Created', max_length=100, verbose_name=(('Created', 'Created'), ('Assigned', 'Assigned'), ('In Progrss', 'In Progrss'), ('Under Review', 'Under Review'), ('Done', 'Done'))),
        ),
    ]
