import time
from celery import shared_task
from django.core.mail import send_mail
from news.models import Subscriber, Post

@shared_task
def send_notification_to_subscribers(news_id):
    try:
        news = Post.objects.get(id=news_id)
        subscribers = Subscriber.objects.all()
        emails = [subscriber.email for subscriber in subscribers]

        send_mail(
            subject=f'Новая новость: {news.title}',
            message=news.content,
            from_email='your_email@example.com',
            recipient_list=emails,
        )
    except Post.DoesNotExist:
        pass


@shared_task
def send_weekly_newsletter():
    print("Weekly newsletter sent!")


@shared_task
def action(some_arg):
    print(f"Action executed with argument: {some_arg}")