"""
URL configuration for student_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import UsersAPI, LoginAPI, RegisterAPI, GetStudentsByClassesAPI, GetClassByLecturerAPI
from myapp.views import  GetStudentByCodeOrNameAPI, GetCourseAndGradeByStudentAPI, UploadGradesCSVAPI, SendMailAPI, LockGradeAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UsersAPI.as_view()),
    path('api/login/', LoginAPI.as_view()),
    path('api/register/', RegisterAPI.as_view()),
    path('api/lecturer/<int:instructor_id>/classes/', GetClassByLecturerAPI.as_view(), name='get-class-by-lecturer'),
    path('api/classes/<int:class_id>/students/', GetStudentsByClassesAPI.as_view(), name='get-students-by-lecturer'),
    path('api/classes/<int:class_id>/student/<str:student_code_or_name>/', GetStudentByCodeOrNameAPI.as_view(), name='get-student-by-code-or-name'),
    path('api/course/<int:student_id>/', GetCourseAndGradeByStudentAPI.as_view(), name='get-course-by-student'),
    path('api/upload-csv/<int:class_id>/', UploadGradesCSVAPI.as_view()),
    path('api/send-mail/', SendMailAPI.as_view()),
    path('api/lock-grade/', LockGradeAPI.as_view()),
]
