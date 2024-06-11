from django.contrib import admin
from .models import Classes, Courses, Enrollments, ForumPosts, Grades, Roles, Users 

admin.site.register(Classes)
admin.site.register(Courses)
admin.site.register(Enrollments)
admin.site.register(ForumPosts)
admin.site.register(Grades)
admin.site.register(Roles)
admin.site.register(Users)
