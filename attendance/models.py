from django.db import models
from datetime import datetime


class Student(models.Model):
    """ Stores student details """

    reg_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.reg_no


class StudentImage(models.Model):
    """ Stores student pictures """

    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE, related_name='studentimage_set')
    image = models.ImageField(upload_to='student/')

    def __str__(self):
        return self.student.reg_no


class Subject(models.Model):
    """ Stores subject details """

    subject_code = models.CharField(max_length=10)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_code


class Attendance(models.Model):
    """ Stores attendance """

    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return 'subject: {} | student: {}'.format(self.subject, self.student)


class Image(models.Model):

    image = models.ImageField(upload_to='student_tmp/')