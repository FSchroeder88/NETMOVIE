from video.tasks import convert_480p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os

@receiver(post_save, sender=Video) #Wird ausgeführt nach dem erstellen eines neuen Videos -> und in apps.py schauen, damit es ausgeführt wird
def video_post_save(sender, instance, created, **kwargs):
    print('Video gespeichert')
    convert_480p(instance.video_file.path)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender,instance,**kwargs):
    """
    Deletes file from filesystem when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)