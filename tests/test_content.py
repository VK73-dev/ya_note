from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestNotesPage(TestCase):
    PAGE_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Алексей Толстой')
        cls.reader = User.objects.create(username='Лев Толстой')
        all_notes = []
        users = (cls.author, cls.reader)
        for user in users:
            for index in range(len(user.get_username())):
                note = Note.objects.create(
                    title=f'Заметки {user} {index}',
                    text='Просто текст.',
                    author=user,)
                print(note)
                note = Note(title=f'Заметки {user} {index}',
                            text='Просто текст.',
                            author=user,)
                all_notes.append(note)
        # Note.objects.bulk_create(all_notes)

    def test_notes_count(self):
        response = self.client.get(self.PAGE_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, len(self.author.get_username()))
