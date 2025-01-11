import logging
from datetime import timedelta
from django.utils.timezone import now

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category, User

logger = logging.getLogger(__name__)


def send_weekly_articles():
    last_week = now() - timedelta(days=7)
    recent_posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = Category.objects.filter(post__in=recent_posts).distinct()

    for category in categories:
        posts_in_category = recent_posts.filter(postCategory=category)
        post_list = "\n".join(
            [f"- {post.title}: http://127.0.0.1:8000{post.get_absolute_url()}" for post in posts_in_category]
        )
        subscribers = User.objects.filter(subscriptions__category=category).values_list('email', flat=True)
        subject = f'Новые статьи в категории "{category.name}" за неделю'
        text_content = f'Список новых статей:\n{post_list}'
        html_content = f'<p>Список новых статей:</p><ul>' + "".join(
            [f'<li><a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a></li>' for post in posts_in_category]
        ) + '</ul>'

        for email in subscribers:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    logger.info("Weekly articles email sent successfully.")


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_articles,
            trigger=CronTrigger(day_of_week="fri", hour=18, minute=0),
            id="send_weekly_articles",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_articles'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour=0, minute=0),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully.")
