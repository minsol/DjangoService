from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializers
# Create your views here.
 
class StudentViewSet(viewsets.ModelViewSet):
    # 指定结果集并设置排序
        queryset = Student.objects.all().order_by('-pk')
    # 指定序列化的类
        serializer_class = StudentSerializers
