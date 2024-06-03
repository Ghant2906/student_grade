# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Classes(models.Model):
    course = models.ForeignKey('Courses', models.DO_NOTHING, blank=True, null=True)
    instructor = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    semester = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classes'


class Courses(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class Enrollments(models.Model):
    class_field = models.ForeignKey(Classes, models.DO_NOTHING, db_column='class_id', blank=True, null=True) 
    student = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enrollments'


class ForumPosts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forum_posts'


class Grades(models.Model):
    enrollment = models.ForeignKey(Enrollments, models.DO_NOTHING, blank=True, null=True)
    midterm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    final = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    additional_grade_1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    additional_grade_2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    additional_grade_3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    draft = models.BooleanField(blank=True, null=True)
    locked = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades'


class Roles(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Users(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    studen_code = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING, blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
