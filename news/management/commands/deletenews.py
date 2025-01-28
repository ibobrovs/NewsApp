from django.core.management.base import BaseCommand, CommandError
from news.models import Post, PostCategory


class Command(BaseCommand):
    help = 'Удаляет новости из категории'

    def add_arguments(self, parser):
        parser.add_argument('PostCategory', type=str, help='Название категории для удаления новостей')

    def handle(self, *args, **options):
        category_name = options['PostCategory']
        answer = input(f'Вы правда хотите удалить все статьи в категории "{category_name}"? yes/no: ').strip().lower()

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Операция отменена'))
            return

        try:
            # Находим категорию по имени
            category = PostCategory.objects.get(name=category_name)

            # Удаляем связанные посты
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Все новости из категории "{category.name}" успешно удалены'))

        except PostCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория "{category_name}" не найдена'))
