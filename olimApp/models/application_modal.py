from django.db import models


class Application(models.Model):
    school_name = models.CharField(max_length=100, unique=True)
    teacher_name = models.CharField(max_length=100, unique=True)
    teacher_email = models.EmailField(unique=True)

    class_3_section_1 = models.CharField(max_length=100, null=True, blank=True)
    class_3_section_2 = models.CharField(max_length=100, null=True, blank=True)
    class_3_section_3 = models.CharField(max_length=100, null=True, blank=True)
    class_4_section_1 = models.CharField(max_length=100, null=True, blank=True)
    class_4_section_2 = models.CharField(max_length=100, null=True, blank=True)
    class_4_section_3 = models.CharField(max_length=100, null=True, blank=True)
    class_4_section_4 = models.CharField(max_length=100, null=True, blank=True)