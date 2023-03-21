from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'author', 'dateCreation']
    list_filter = ('author', 'dateCreation')


admin.site.register(Post, PostAdmin)