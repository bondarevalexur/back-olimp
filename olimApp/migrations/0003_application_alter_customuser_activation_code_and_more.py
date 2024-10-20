# Generated by Django 5.1.1 on 2024-10-08 18:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olimApp', '0002_customuser_activation_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=100, unique=True)),
                ('teacher_name', models.CharField(max_length=100, unique=True)),
                ('teacher_email', models.EmailField(max_length=254, unique=True)),
                ('class_3_section_1', models.CharField(blank=True, max_length=100, null=True)),
                ('class_3_section_2', models.CharField(blank=True, max_length=100, null=True)),
                ('class_3_section_3', models.CharField(blank=True, max_length=100, null=True)),
                ('class_4_section_1', models.CharField(blank=True, max_length=100, null=True)),
                ('class_4_section_2', models.CharField(blank=True, max_length=100, null=True)),
                ('class_4_section_3', models.CharField(blank=True, max_length=100, null=True)),
                ('class_4_section_4', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='activation_code',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
