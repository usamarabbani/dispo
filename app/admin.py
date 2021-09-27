from django.contrib import admin
from .models import Post, PostLike, Follow

# Register your models here.
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Follow)
