from django.shortcuts import render
from blogapp.models import Blog
from blogapp.serializer import BlogSerializer, UpdateUserProfileSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UpdateUserProfileSerializer(user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user = request.user
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def blog_list(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data) 


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blog(request, blog_id):
    user = request.user
    blog = Blog.objects.get(id=blog_id)
    if blog.author != user:
        return Response({"error": "You are not the author and do not have permission to edit this blog."}, status=status.HTTP_403_FORBIDDEN)
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog(request, blog_id):
    user = request.user
    blog = Blog.objects.get(id=blog_id)
    if blog.author != user:
        return Response({"error": "You are not the author and do not have permission to edit this blog."}, status=status.HTTP_403_FORBIDDEN)
    blog.delete()
    return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)