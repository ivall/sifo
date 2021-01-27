from django.contrib import admin

from .models import Video, Category, Link, Episode

admin.site.register(Video)
admin.site.register(Category)
admin.site.register(Link)
admin.site.register(Episode)
