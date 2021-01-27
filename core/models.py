from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=26)
    type = models.CharField(max_length=16)  # "date" or "language" or "category"


class Video(models.Model):
    name = models.CharField(max_length=46)
    description = models.CharField(max_length=800)
    image = models.URLField()
    categories = models.ManyToManyField(Category)
    type = models.CharField(max_length=6)  # "movie" or "series"
    seasons = models.IntegerField(null=True)  # only if type is "series"
    approved = models.BooleanField(default=False)


class Episode(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    season = models.IntegerField()
    episode = models.IntegerField()
    title = models.CharField(max_length=128)


class Link(models.Model):
    url = models.URLField()
    service = models.CharField(max_length=32)  # "openload" or "vidoza"
    quality = models.CharField(max_length=5)
    language = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, null=True)  # only for type of video "series"
    approved = models.BooleanField(default=False)
