from django.contrib import admin
from app.models import *
admin.site.register(Users)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(BlogTag)