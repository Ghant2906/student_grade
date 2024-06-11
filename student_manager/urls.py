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
from myapp.views import UsersAPI, LoginAPI, RegisterAPI, GetStudentsByClassesAPI, GetClassByLecturerAPI, GetCommentByPostAPI, CreateCommentAPI
from myapp.views import  GetStudentByCodeOrNameAPI, GetCourseAndGradeByStudentAPI, UploadGradesCSVAPI, LockGradeAndSendMail, GetAllPostAPI, CreatePostAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UsersAPI.as_view()),
    ### api dang nhap
    ### input: email, password
    ### output: refresh token, access token, userInfo
    path('api/login/', LoginAPI.as_view()),
    ### api dang ky
    ### input: email, password, full_name, avatar_url, student_code
    ### output: id user, message successfully
    path('api/register/', RegisterAPI.as_view()),
    ### api lay danh sach lop hoc giang vien do dam nhan
    ### input: thay <int:instructor_id> bang id cua giang vien
    ### output: [{id, course{id, name, description}, year, semester, instructor}, {id, course{id, name, description}, year, semester, instructor}, ...]
    path('api/lecturer/<int:instructor_id>/classes/', GetClassByLecturerAPI.as_view(), name='get-class-by-lecturer'),
    ### api lay danh sach sinh vien trong lop do
    ### input: thay <int:class_id> bang id lop do
    ### output: id, email, full_name, studen_code, role, avatar_url
    path('api/classes/<int:class_id>/students/', GetStudentsByClassesAPI.as_view(), name='get-students-by-lecturer'),
    ### api lay thong tin va diem cua user theo lop va ma sinh vien hoac ten sinh vien
    ### input: thay <int:class_id> bang id lop va <str:student_code_or_name> bang ten hoac ma sinh vien
    ### output: student{id, email, full_name, studen_code, role, avatar_url}, course{id, name, description}, midterm, final, additional_grade_1, additional_grade_2, additional_grade_3
    path('api/classes/<int:class_id>/student/<str:student_code_or_name>/', GetStudentByCodeOrNameAPI.as_view(), name='get-student-by-code-or-name'),
    ### api lay toan bo thong tin course va diem cua course do theo sinh vien
    ### input: thay <int:student_id> bang id sinh vien
    ### output: [{course{id, name, description}, midterm, final, additional_grade_1, additional_grade_2, additional_grade_3}, {course{id, name, description}, midterm, final, additional_grade_1, additional_grade_2, additional_grade_3}, ...]
    path('api/course/<int:student_id>/', GetCourseAndGradeByStudentAPI.as_view(), name='get-course-by-student'),
    ### api cap nhat diem sinh vien bang file csv
    ### input: gui file csv trong body voi ten "file", thay <int:class_id> bang id lop do
    ### output: message successfully
    path('api/upload-csv/<int:class_id>/', UploadGradesCSVAPI.as_view()),
    ### api gui mail
    ### input: trong body gui class_id bang id lop do
    ### output: message khoa diem va sen mail thanh cong
    path('api/lock_grade/', LockGradeAndSendMail.as_view()),
    ### api lay toan bo bai viet
    ### input: none
    ### output: [{id, author{id, email, full_name, studen_code, role, avatar_url}, title, content, created_at, updated_at, class_field}, [{id, author{id, email, full_name, studen_code, role, avatar_url}, title, content, created_at, updated_at, class_field}, ...]
    path('api/post/', GetAllPostAPI.as_view()),
    ### api them bai viet
    ### input: trong body gui author_id bang id user, title, content
    ### output: thong tin bai viet moi duoc tao
    path('api/create-post/', CreatePostAPI.as_view()),
    ### api lay comment theo bai viet
    ### input: thay <int:post_id> bang id bai viet
    ### output: [{id, author{id, email, full_name, studen_code, role, avatar_url}, content, created_at, post}, {id, author{id, email, full_name, studen_code, role, avatar_url}, content, created_at, post}, ...]
    path('api/post/<int:post_id>/comment/', GetCommentByPostAPI.as_view()),
    ### api them comment
    ### input: trong body gui author_id bang id user, content, post_id bang id bai viet
    ### output: thong tin comment duoc tao
    path('api/create-comment/', CreateCommentAPI.as_view()),
]
