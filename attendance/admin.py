from django.contrib import admin

from attendance.models import Student, StudentImage, Subject, StudentImage, Attendance, Image


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'reg_no', 'name']


@admin.register(StudentImage)
class StudentImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
