from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Replay

@receiver(pre_save, sender=Replay)
def my_handler(sender, instance, created, **kwargs):
    if instance.status:
        mail = instance.author.email
        send_mail(
            'Subject here',
            'Here is the message.',
            'host@mail.ru'
            [mail],
            fail_silently=False,
        )
    mail = instance.article.author.email
    send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru'
        [mail],
        fail_silently=False,
    )