# import json
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from first_app.models import Student
# # Create your views here.

# @csrf_exempt
# def get_students(request):
#     if request.method == 'GET':
#         students = Student.objects.all() # <==> select * from students
#         print(students) # QuerySet<[]>
#         students_list = []
#         for student in students:
#             students_list.append({
#                 'id': student.id,
#                 'first_name': student.first_name,
#                 'last_name': student.last_name,
#                 'email':student.email,
#                 'age':student.age,
#                 'is_active':student.is_active,
#                 'created_at':student.created_at,
#                 "classe":student.classe
#             })
#         return JsonResponse({
#             'students':students_list,
#             'count':len(students_list)
#         })
        
#     return JsonResponse({'error':'Method not Allowed'}, status=405)

# def get_student(request,pk):
#     if request.method == 'GET':
#         student = Student.objects.get(id = pk)
#         # select * from student where id = pk
#         print(student)
#         student_data={
#             "id":student.id,
#             "first_name":student.first_name,
#             "last_name":student.last_name,
#             "email":student.email,
#             "age":student.age,
#             "is_active":student.is_active,
#             # "created_at":student.created_at,
#             "classe":student.classe
#         }

#         return JsonResponse({
#             "student":student_data,
#             'success':True
#         })
#     return JsonResponse({'error':'Method not Allowed'}, status=405)

# @csrf_exempt
# def create_student(request):
#     data = json.loads(request.body)
#     # validate required fields
#     required_fields = ['first_name','last_name','email','age','classe']
#     for field in required_fields:
#         if field not in data:
#             return JsonResponse({
#                 "error": f"Missing required field: {field}",
#                 "success": False
#             },status=400)
        
#     student = Student.objects.create(
#         first_name = data['first_name'],
#         last_name = data['last_name'],
#         email = data['email'],
#         age = data['age'],
#         classe = data['classe']
#     )
#     """
#     insert into students (first_name, last_name, age,email,is_active,classe)
#     values ('salma','tahri',36,'s.tahri@email.com',9)
#     """
#     student_data={
#         "id":student.id,
#         "first_name":student.first_name,
#         "last_name":student.last_name,
#         "email":student.email,
#         "age":student.age,
#         "is_active":student.is_active,
#         "classe":student.classe
#     }
#     return JsonResponse({
#         "message":"student added successfully",
#         "student":student_data,
#         "success":True
#     },status = 201) # or 200

# @csrf_exempt
# def delete_student(request, student_id):
#     if request.method == "DELETE":
#         student = Student.objects.get(id=student_id)
#         student.delete()
#         print("another print to test git branch")
#         print('dddd')
#         """
#         delete from students where id = student_id
#         """

#         return JsonResponse({
#             "message":"Student deleted successfully",
#             "success":True
#         })
    
#     return JsonResponse({
#         "error":"Method Not Allowed"
#     }, status=405)

# @csrf_exempt
# def update_student(request,pk):
#     if request.method == "PUT":
#         student = Student.objects.get(id = pk)
#         data = json.loads(request.body)
#         print("test git status")
#         if 'first_name' in data:
#             student.first_name = data['first_name']
#         if 'last_name' in data:
#             student.last_name = data['last_name']
#         if 'email' in data:
#             student.email = data['email']
#         if 'age' in data:
#             student.age = data['age']
#         if 'is_active' in data:
#             student.is_active = data['is_active']
#         if 'classe' in data:
#             student.classe = data['classe']
        
#         student.save()

#         """
#         update students
#         SET
#         first_name = "ahmed"
#         last_name = "ben salah"
#         email = "a.ben_salem@email.com"
#         age = 21
#         is_active = false
#         classe = 9

#         where id = pk;
#         """

#         student_data = {
#             'id': student.id,
#             'first_name':student.first_name,
#             'last_name': student.last_name,
#             "email":student.email,
#             'age':student.age,
#             'is_active':student.is_active,
#             'classe':student.classe
#         }
#         return JsonResponse({
#             'message':"student updated successfully",
#             "student":student_data,
#             "success":True
#         })

#     return JsonResponse({
#         "error": "method not allowed"
#     },status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
from .serializers import StudentSerializer
import json

@csrf_exempt
@require_http_methods(['GET'])
def get_students(request):
    """GET: List all students"""
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return JsonResponse({
        "students":serializer.data,
        "count":len(serializer.data)
    })

@csrf_exempt
@require_http_methods(['GET'])
def get_student(request, student_id):
    """GET: retrieve a specific student"""
    try:
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student)
        return JsonResponse({
            "student":serializer.data,
            "success":True
        })
    except Student.DoesNotExist:
        return JsonResponse({
            "error": "Student not found",
            "success":False
        },status = 404)
    
@csrf_exempt
@require_http_methods(['POST'])
def create_student(request):
    """POST: create a new student"""
    # print({"request.body":request.body})
    json_data = json.loads(request.body)
    # print({"json_data":json_data})
    # print({"name":json_data['first_name']})
    serializer = StudentSerializer(data=json_data)
    if serializer.is_valid():
        student = serializer.save()
        student_data = StudentSerializer(student).data
        return JsonResponse({
            "message":"student created successfully",
            "student":student_data,
            "success":True
        })
    else:
        return JsonResponse({
            "error":serializer.errors,
            "success":False
        },status = 400)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_student(request, pk):
    """DELETE: remove a student"""
    try:
        student = Student.objects.get(id=pk)
        student.delete()
        return JsonResponse({
            "message": "student deleted successfully",
            "success":True
        })
    except Student.DoesNotExist:
        return JsonResponse({
            "error": "student not found",
            "success":False
        },status=404)
    

@csrf_exempt
@require_http_methods(['PUT','PATCH'])
def update_student(request, pk):
    """PUT/PATCH: update a student"""
    json_data = json.loads(request.body)
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return JsonResponse({
            "error": 'student not found',
            "success":False
        },status=404)
    
    serializer = StudentSerializer(student, data=json_data)
    if serializer.is_valid():
        student = serializer.save()
        student_data = StudentSerializer(student).data
        return JsonResponse({
            "message":"student updated successfully",
            "student":student_data,
            "success":True
        })

    return JsonResponse({
        "error":serializer.errors,
        "success":False
    },status=400)