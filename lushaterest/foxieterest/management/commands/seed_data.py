from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction
from foxieterest.models import User, Comment, Pin, Board

class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            """Проверяем, есть ли уже пользователи """
            if User.objects.exists():
                 self.stdout.write(self.style.WARNING('Данные уже существуют. Пропускаем...'))
                 return

            self.stdout.write(self.style.SUCCESS('Создание тестовых данных...'))

            # создаем тестового пользователя
            user = User.objects.create(
                username = 'VoidWeaver',
                email = 'aboutme@example.com',
                password = make_password('testpass123'),  # Хэшируем пароль
                settings={'theme': 'light', 'notifications': True}
            )
            self.stdout.write(f'Создан пользователь: {user.username}')

            # Создаем доски
            boards = []
            board_data = [
                ('Зверятки', 'Милые представители животного мира ^^', False),
                ('Мемы', '', True),
                ('Эстетика', 'Приятные глазу видео и изображения', False),
            ]
            for title, desc, is_private in board_data:
                board = Board.objects.create(
                    title=title,
                    description=desc,
                    is_private=is_private
                    )
                boards.append(board)
                self.stdout.write(f'Создан проект: {board.title}')

            # Создаем посты
            pins_data = [
                {
                    'title': 'Лисица Фенёк',
                    'description': 'Пушистая песчаная лисичка)',
                    # 'status': Task.Status.NEW,
                    # 'priority': Task.Priority.MEDIUM,
                    'is_private': False,
                    'boards': [boards[0], boards[2]]  # Зверятки, Эстетика
                },
                {
                    'title': 'Гнездо голубя',
                    'description': 'Как строят гнезда другие птицы: 🕊, тем временем голубь:',
                    'is_private': False,
                    'boards': [boards[1]]  # Мемы
                },
                {
                    'title': 'Сигнальные шпили Rain World',
                    'description': 'Best location ever 🤩',
                    'is_private': False,
                    'boards': [boards[2]]  # Эстетика
                },
                {
                    'title': 'Chimney Canopy jump',
                    'description': 'Just a little over-jumped xD',
                    'is_private': False,
                    'boards': [boards[1]]  # Мемы
                },
            ]

            for pin_data in pins_data:
                boards_list = pin_data.pop('boards')
                pin = Pin.objects.create(user=user, **pin_data)
                pin.boards.set(boards_list)  # Добавляем теги через many-to-many
                self.stdout.write(f'Создан пин: {pin.title}')

            user.boards.set(boards) # присваиваем пользователю доски

            # Создаем комментарии
            comments = []
            contents = ['Meow soounds))', 'Literally моя курсовая', 'Киты хорошие)', 'Когда не рассчитал миллиметраж, пх']
            counter = 0
            for cont in contents:
                comment = Comment.objects.create(user=user, content=cont, pin=Pin.objects.get(pk=counter))
                comments.append(comment)  # Исправлено: добавляем каждый тег в список
                self.stdout.write(f'Создан комментарий: {comment.content}')
                counter += 1

            # Выводим итоговую статистику (вынесено за цикл)
            self.stdout.write(self.style.SUCCESS(
                f'Успешно создано: '
                f'{User.objects.count()} пользователь, '
                f'{Board.objects.count()} досок, '
                f'{Pin.objects.count()} постов, '
                f'{Comment.objects.count()} комментариев'
            ))