from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from board.tasks import send_notification_to_subscribers


def send_email_notifications(subject, text_content, html_content, recipient_emails):
    """
    Общая функция для отправки email-уведомлений.
    """
    for email in recipient_emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Post)
def product_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category__in=instance.postCategory.all()
    ).values_list('email', flat=True)

    subject = f'Новая статья в категории {", ".join(c.name for c in instance.postCategory.all())}'
    text_content = (
        f'Статья: {instance.title}\n'
        f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Статья: {instance.title}<br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на статью</a>'
    )

    send_email_notifications(subject, text_content, html_content, emails)


@receiver(post_save, sender=Post)
def send_news_notification(sender, instance, created, **kwargs):
    if created:
        send_notification_to_subscribers.delay(instance.id)
