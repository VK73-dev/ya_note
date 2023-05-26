from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestNotesPage(TestCase):
    PAGE_URL = reverse('notes:list')
    COUNT_NOTES = 10

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Alex')
        cls.reader = User.objects.create(username='Michael')

        users = (cls.author, cls.reader)
        all_notes = []
        for user in users:
            for index in range(cls.COUNT_NOTES):
                note = Note(
                    title=f'Заметка {user} {index}',
                    slug=f'note_{user}_{index}',
                    text='Просто текст.',
                    author=user,
                )
                all_notes.append(note)
        Note.objects.bulk_create(all_notes)

    def test_notes_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.PAGE_URL)
        object_list = response.context['object_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, self.COUNT_NOTES)
