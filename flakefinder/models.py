from django.db import models
from django.utils import timezone


class Chip(models.Model):
    name = models.CharField(max_length=2000)
    date_created = models.DateTimeField("date created", default=timezone.now)

    original_image = models.ImageField(upload_to="", default="example.jpg")
    labelled_image = models.ImageField(
        upload_to="",
        default="example_labelled.jpg"
    )

    num_flakes = models.IntegerField(default=0)
    owner = models.CharField(max_length=200, default="")
