from django.contrib import admin
from .models import Profile, StatusMessage, Image, StatusImage, Friend

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)