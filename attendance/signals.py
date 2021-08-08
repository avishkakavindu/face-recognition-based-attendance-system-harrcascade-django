import os
from django.conf import settings as django_settings
import cv2
from django.db.models.signals import post_save
from django.dispatch import receiver
from attendance.models import Image, Student


@receiver(post_save, sender=Image)
def mark_attendance(sender, instance, **kwargs):
    pass