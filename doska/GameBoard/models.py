from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('bayers', 'Торговцы'),
        ("gildemaster", 'Гилдмастеры'),
        ('quest', 'Квестигиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    category = models.CharField(max_length=8, choices=TYPE, default='tank')
    upload = models.FileField(upload_to='uploads/')


class Replay(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
