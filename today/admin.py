from django.contrib import admin
from today.models import *

# Register your models here.
admin.site.register(Schedule)
admin.site.register(Hashtag)
admin.site.register(Post)
admin.site.register(Comment)