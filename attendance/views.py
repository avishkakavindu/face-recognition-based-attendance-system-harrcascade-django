import cv2
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic, View
from mlxtend.image.extract_face_landmarks import detector
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status, generics
from attendance.models import StudentImage, Student, Attendance, Subject
from attendance.serializers import StudentSerializer, StudentImageSerializer, AttendanceSerializer
import os
from PIL import Image
import numpy as np
from django.conf import settings as django_settings
from django.shortcuts import redirect
from rest_framework.response import Response


class RegisterView(generic.TemplateView):
    """ Registration view """

    template_name = 'index.html'


class AttendanceView(generic.TemplateView):
    """ Attendance view """

    template_name = 'attendance.html'

    def get_context_data(self, **kwargs):
        """ return the details of past attendance of the students """
        context = super(AttendanceView, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['attendance'] = Attendance.objects.all()
        return context


class TrainView(View):
    """ Train view """

    def get(self, request, *args, **kwargs):
        import pandas as pd

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        student_images = pd.DataFrame(StudentImage.objects.values('student', 'image'))

        student_ids = student_images['student']
        image_paths = student_images['image']
        face_samples = []
        ids = []

        for path_index, image_path in enumerate(image_paths):

            PIL_img = cv2.imread(os.path.join(django_settings.MEDIA_ROOT, image_path), 0)
            img_numpy = np.array(PIL_img, 'uint8')

            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y + h, x:x + w])
                ids.append(student_ids[path_index])

            recognizer.train(face_samples, np.array(ids))
            recognizer.write('static/model/trainer.yml')

        return redirect('index')


class StudentRegisterAPIView(CreateAPIView):
    """ Register the student """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentImageAPIView(CreateAPIView):
    queryset = StudentImage.objects.all()
    serializer_class = StudentImageSerializer


class AttendanceAPIVIew(generics.GenericAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        serializer = AttendanceSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read('static/model/trainer.yml')
            cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')

            face_cascade = cv2.CascadeClassifier(cascade_path)

            img_path = str(obj.image)

            from django.conf import settings as django_settings

            image = cv2.imread(os.path.join(django_settings.MEDIA_ROOT, img_path), 0)

            faces = face_cascade.detectMultiScale(
                image,
                scaleFactor=1.2,
                minNeighbors=5,
            )

            context = {
                'success': len(faces) != 0,
                'student_id': None,
                'message': None
            }

            sts = status.HTTP_401_UNAUTHORIZED

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                id, confidence = recognizer.predict(image[y:y + h, x:x + w])

                if confidence < 100:
                    # get recognize student
                    student = Student.objects.get(id=id)
                    # get the subject
                    subject = Subject.objects.get(subject_code=request.data['subject'])
                    # save attendance
                    attendance = Attendance.objects.create(
                        subject=subject,
                        student=student
                    )
                    # attendance details
                    attendance_data = {
                        'subject': attendance.subject.subject_code,
                        'student': attendance.student.reg_no,
                        'timestamp': str(attendance.timestamp)
                    }

                               # prepare response
                    context['student_id'] = id
                    context['message'] = "Face Detected and Recognized! Attendance Marked!"
                    context['attendance'] = attendance_data
                    sts = status.HTTP_200_OK
                    print('\n\n\n Detected:', id)
                else:
                    context['success'] = False
                    context['message'] = "Unidentified Face Detected Please Register!"
                    sts = status.HTTP_401_UNAUTHORIZED
                    print('\n\n\nUnable to detect')

            return Response(context, status=sts)

