from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=11, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.CharField(max_length=2048)
    publishedAt = models.DateTimeField(db_index=True)
