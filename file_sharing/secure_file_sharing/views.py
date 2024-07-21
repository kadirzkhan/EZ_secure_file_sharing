# filesharing/views.py
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, File
from .serializers import UserSerializer, FileSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from cryptography.fernet import Fernet


# Utility function to create JWT token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Ops User Login
@api_view(['POST'])
def ops_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None and user.user_type == 'ops':
        update_last_login(None, user)
        token = get_tokens_for_user(user)
        return Response({'token': token}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials or not an Operation User'}, status=status.HTTP_401_UNAUTHORIZED)

# Upload File
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    if request.user.user_type != 'ops':
        return Response({'error': 'Only Ops Users can upload files'}, status=status.HTTP_403_FORBIDDEN)
    
    file = request.FILES['file']
    if not file.name.endswith(('.pptx', '.docx', '.xlsx')):
        return Response({'error': 'Only pptx, docx, and xlsx files are allowed'}, status=status.HTTP_400_BAD_REQUEST)
    
    new_file = File(uploader=request.user, file=file)
    new_file.save()
    
    return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)

# Client User Signup
@api_view(['POST'])
def client_signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = User.objects.create_user(username=username, email=email, password=password, user_type='client')
    user.save()
    
    # Generate email verification link
    verification_code = get_random_string(20)
    verification_link = f'{settings.DOMAIN}/verify-email/{verification_code}'
    send_mail(
        'Verify your email',
        f'Click the link to verify your email: {verification_link}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    
    return Response({'message': 'Signup successful. Verification email sent.'}, status=status.HTTP_201_CREATED)

# Verify Email
@api_view(['GET'])
def verify_email(request, code):
    # Logic to verify email using the code
    return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

# Client User Login
@api_view(['POST'])
def client_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None and user.user_type == 'client':
        update_last_login(None, user)
        token = get_tokens_for_user(user)
        return Response({'token': token}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials or not a Client User'}, status=status.HTTP_401_UNAUTHORIZED)

# List all uploaded files
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    if request.user.user_type != 'client':
        return Response({'error': 'Only Client Users can list files'}, status=status.HTTP_403_FORBIDDEN)
    
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Download File
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    if request.user.user_type != 'client':
        return Response({'error': 'Only Client Users can download files'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        file = File.objects.get(id=file_id)
        key = settings.ENCRYPTION_KEY  # Should be set in your settings
        fernet = Fernet(key)
        encrypted_url = fernet.encrypt(file.file.url.encode()).decode()
        return Response({'download-link': encrypted_url, 'message': 'success'}, status=status.HTTP_200_OK)
    except File.DoesNotExist:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
