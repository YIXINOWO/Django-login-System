from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from .models import UserInfo
from .serializers import UserSerializer, UserCreateSerializer

# Swagger参数定义
user_response = openapi.Response('response description', UserInfo)

# Create your views here.

def add_user(request):
    UserInfo.objects.create(username="admin", password="admin", age=18)
    return HttpResponse("User added successfully!")

def delete_user(request):
    UserInfo.objects.filter(username="admin").delete()
    return HttpResponse("User deleted successfully!")

@swagger_auto_schema(
    method='post',
    request_body=UserCreateSerializer,
    responses={200: UserSerializer}
)
@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            age = data.get('age')
            email = data.get('email')
            
            if UserInfo.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already exists'})
            
            if UserInfo.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already exists'})
            
            user = UserInfo.objects.create(
                username=username,
                password=make_password(password),
                age=age,
                email=email
            )
            serializer = UserSerializer(user)
            return Response({'status': 'success', 'user': serializer.data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@swagger_auto_schema(
    method='post',
    request_body=UserCreateSerializer,
    responses={200: UserSerializer}
)
@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            try:
                user = UserInfo.objects.get(username=username)
                if check_password(password, user.password):
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login successful',
                        'user': {
                            'username': user.username,
                            'email': user.email,
                            'age': user.age
                        }
                    })
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid password'})
            except UserInfo.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, description="页码", type=openapi.TYPE_INTEGER)
    ],
    responses={200: UserSerializer(many=True)}
)
@csrf_exempt
@api_view(['GET'])
def get_all_users(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', 1))
            page_size = 5
            
            total_users = UserInfo.objects.count()
            start = (page - 1) * page_size
            end = start + page_size
            
            users = UserInfo.objects.all()[start:end]
            serializer = UserSerializer(users, many=True)
            
            return Response({
                'status': 'success',
                'users': serializer.data,
                'total': total_users,
                'total_pages': (total_users + page_size - 1) // page_size
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@swagger_auto_schema(
    method='put',
    request_body=UserCreateSerializer,
    responses={200: UserSerializer}
)
@csrf_exempt
@api_view(['PUT'])
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = UserInfo.objects.get(id=user_id)
            
            if data.get('username') != user.username and UserInfo.objects.filter(username=data.get('username')).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already exists'})
            
            if data.get('email') != user.email and UserInfo.objects.filter(email=data.get('email')).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already exists'})
            
            user.username = data.get('username', user.username)
            if data.get('password'):
                user.password = make_password(data.get('password'))
            user.email = data.get('email', user.email)
            user.age = data.get('age', user.age)
            user.save()
            
            serializer = UserSerializer(user)
            return Response({'status': 'success', 'user': serializer.data})
        except UserInfo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@swagger_auto_schema(
    method='delete',
    responses={200: openapi.Response(description='User deleted successfully')}
)
@csrf_exempt
@api_view(['DELETE'])
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = UserInfo.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})
        except UserInfo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

