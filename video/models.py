
from django.db import models
from datetime import date


class Video(models.Model):
    NEUERSCHEINUNGEN = 'Neuerscheinungen'
    SERIEN = 'Serien'
    FILME = 'Filme'
    speciality_CHOICES = [
        (NEUERSCHEINUNGEN, 'Neuerscheinungen'),
        (SERIEN, 'Serien'),
        (FILME, 'Filme'),
    ]

    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    image_file = models.FileField(
        upload_to='video-cover', blank=True, null=True)
    speciality = models.CharField(max_length=20, choices=speciality_CHOICES, default=FILME)

    def __str__(self):
        return self.title
