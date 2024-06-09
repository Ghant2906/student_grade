from rest_framework.views import APIView
from myapp.models import Users, Classes, Enrollments, Grades, Courses
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, ClassesSeriralizer, GradeSerializer, StudentGradeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Q
import pandas as pd
from django.db import transaction
from rest_framework.parsers import MultiPartParser
from django.core.mail import send_mail

class UsersAPI(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class LoginAPI(APIView):
    def post(self, request):
        data_login = LoginSerializer(data=request.data)
        if not data_login.is_valid():
            return Response("du lieu gui len sai roi", status=status.HTTP_400_BAD_REQUEST)
        email = data_login.data['email']
        password = data_login.data['password']
        user_info = Users.objects.filter(email=email, password=password).values(
            'id', 'email', 'full_name', 'avatar_url', 'created_at').first()
        if user_info is None:
            return Response("tai khoan hoac mat khau khong chinh xac", status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(Users.objects.get(id=user_info['id']))
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_info': user_info
        }, status=status.HTTP_200_OK)
    
class RegisterAPI(APIView):
    def post(self, request):
        data_register = RegisterSerializer(data=request.data)
        if not data_register.is_valid():
            return Response("du lieu gui len sai roi", status=status.HTTP_400_BAD_REQUEST)
        email = data_register.data['email']
        password = data_register.data['password']
        full_name = data_register.data['full_name']
        avatar_url = data_register.data['avatar_url']
        student_code = data_register.data['student_code']
        user_info = Users.objects.create(email=email, password=password, full_name=full_name, avatar_url=avatar_url, studen_code=student_code, role_id=3, created_at=datetime.now(), is_active= True)
        return Response({"id": user_info.id, "message": "Đăng ký thành công"}, status=status.HTTP_200_OK)
    

class GetStudentsByClassesAPI(APIView):
    def get (self, request, class_id):
        classes = get_object_or_404(Classes, pk=class_id)
        enrollments = Enrollments.objects.filter(class_field=classes)
        students = Users.objects.filter(id__in=enrollments.values('student_id'))
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)
    
class GetClassByLecturerAPI(APIView):
    def get (self, request, instructor_id):
        instructor = get_object_or_404(Users, pk=instructor_id)
        classes = Classes.objects.filter(instructor=instructor)
        serializer = ClassesSeriralizer(classes, many=True)
        return Response(serializer.data)
    
class GetStudentByCodeOrNameAPI(APIView):
    def get (self, request, class_id, student_code_or_name):
        users = Users.objects.filter(
            (Q(studen_code=student_code_or_name) | Q(full_name=student_code_or_name)) & Q(role_id=3)
        )
        enrollments = Enrollments.objects.filter(student__in=users, class_field_id=class_id)
        grade_of_students = Grades.objects.filter(enrollment__in=enrollments)
        serializer = StudentGradeSerializer(grade_of_students, many=True)
        return Response(serializer.data)

class GetCourseAndGradeByStudentAPI(APIView):
    def get (self, request, student_id):
        student = get_object_or_404(Users, pk=student_id)
        gradeOfStudent = Grades.objects.filter(enrollment__student=student)
        serializer = GradeSerializer(gradeOfStudent, many=True)
        return Response(serializer.data)
    
class UploadGradesCSVAPI(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, class_id):
        csv_file = request.FILES['file']
        data = pd.read_csv(csv_file)

        with transaction.atomic():
            for index, row in data.iterrows():
                student_id = row['student_id']
                enrollment = Enrollments.objects.get(student_id=student_id, class_field_id=class_id)
                Grades.objects.update_or_create(
                    enrollment=enrollment,
                    defaults={
                        'midterm': float(row['midterm']),
                        'final': float(row['final']),
                        'additional_grade_1': float(row.get('additional_grade_1')),
                        'additional_grade_2': float(row.get('additional_grade_2')),
                        'additional_grade_3': float(row.get('additional_grade_3')),
                        'draft': True,
                        'locked': False
                    }
                )
        return Response({"message": "Grades uploaded successfully"}, status=status.HTTP_201_CREATED)

class LockGradeAPI(APIView):
    def get_student_email_by_grade_id(self, grade_id):
        enrollments_id = Grades.objects.get(pk=grade_id).enrollment_id
        student_id = Enrollments.objects.get(pk=enrollments_id).student_id
        email = Users.objects.get(pk=student_id).email
        return email
    
    def get_course_name_by_grade_id(self, grade_id):
        enrollments_id = Grades.objects.get(pk=grade_id).enrollment_id
        class_id = Enrollments.objects.get(pk=enrollments_id).class_field_id
        course_id = Classes.objects.get(pk=class_id).course_id
        course_name = Courses.objects.get(pk=course_id).name
        return course_name
    
    def post(self, request):
        grade_id = request.data.get('grade_id')
        grade = get_object_or_404(Grades, pk=grade_id)
        grade.locked = True
        grade.draft = False
        grade.save()

        email_student = self.get_student_email_by_grade_id(grade_id)
        course_name = self.get_course_name_by_grade_id(grade_id)
        subject = 'Thông báo đã có điểm môn ' + course_name
        message = 'Thông báo đã có điểm chi tiết của môn ' + course_name + ', sinh viên có thể vào xem điểm.'
        send_mail(
                subject,
                message,    
                'thaithang2906@gmail.com',
                [email_student],
                fail_silently=False,
            )
        return Response({"message": "Grade locked and Email sent successfully"}, status=status.HTTP_200_OK)
    
class SendMailAPI(APIView):
    def get_student_emails_by_class(self, class_id):
        try:
            class_instance = Classes.objects.get(pk=class_id)  
            enrollments = Enrollments.objects.filter(class_field=class_instance)
            user_ids = enrollments.values_list('student', flat=True)
            emails = Users.objects.filter(id__in=user_ids).values_list('email', flat=True)
            return list(emails)
        except Classes.DoesNotExist:
            return []
        
    def lock_grades_by_class(self, class_id):
        class_instance = get_object_or_404(Classes, pk=class_id)
        enrollments_list = Enrollments.objects.filter(class_field=class_instance)
        enrollments_id_list = enrollments_list.values_list('id', flat=True)
        grade_list = Grades.objects.filter(enrollment_id__in=enrollments_id_list)
        for grade in grade_list:
            grade.draft = False
            grade.locked = True
            grade.save()
        return True
    
    def post(self, request):
        class_id = request.data.get('class_id')
        self.lock_grades_by_class(class_id)
        class_instance = get_object_or_404(Classes, pk=class_id)
        course_name = class_instance.course.name
        subject = 'Thông báo đã có điểm môn ' + course_name
        message = 'Thông báo đã có điểm chi tiết của môn ' + course_name + ', sinh viên có thể vào xem điểm.'
        recipient_list = self.get_student_emails_by_class(class_id)
        if recipient_list:
            send_mail(
                subject,
                message,    
                'thaithang2906@gmail.com',
                recipient_list,
                fail_silently=False,
            )
            return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No emails found or class does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
