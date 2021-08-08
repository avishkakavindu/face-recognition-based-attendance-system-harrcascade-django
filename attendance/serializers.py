import os

import cv2
from rest_framework import serializers
from attendance.models import StudentImage, Student, Attendance, Subject, Image
from drf_extra_fields.fields import Base64ImageField
import base64


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentImageSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    image = Base64ImageField()

    class Meta:
        model = StudentImage
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    subject = serializers.IntegerField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Image
        fields = '__all__'
