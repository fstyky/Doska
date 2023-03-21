from celery import shared_task
from django.contrib.auth.models import User
from .models import Post, Replay
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone


@shared_task
def replay_send_email(respond_id):
    rep = Replay.objects.get(id=respond_id)
    send_mail(
        subject=f'MMORPG Billboard: новый отклик на объявление!',
        message=f'Доброго дня, {rep.post.author}, ! На ваше объявление есть новый отклик!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/responses/{rep.post.id}',
        from_email='newsportal272@gmail.com',
        recipient_list=[rep.post.author.email, ],
    )


@shared_task
def replay_accept_send_email(response_id):
    rep = Replay.objects.get(id=response_id)
    print(rep.post.author.email)
    send_mail(
        subject=f'GameBoard: Принято!',
        message=f'Приветсвуем, {rep.author}, Автор объявления {rep.post.title} утвердил Ваш отклик!',
        from_email='fstyky@gmail.com',
        recipient_list=[rep.post.author.email, ],
    )


@shared_task
def send_mail_in_week():
    now = timezone.now()
    list_week_posts = list(Post.objects.filter(dateCreation__gte=now - timedelta(days=7)))
    if list_week_posts:
        for user in User.objects.filter():
            print(user)
            list_posts = ''
            for post in list_week_posts:
                list_posts += f'\n{post.title}\nhttp://127.0.0.1:8000/post/{post.id}'
            send_mail(
                subject=f'Объявления на этой неделе',
                message=f'Приветсвуем, {user.username}!\nПредлагаем Вам ознакомиться с новыми объявлениями, '
                        f'появившимися за последние 7 дней:\n{list_posts}',
                from_email='fstyky@gmail.com',
                recipient_list=[user.email, ],
            )