from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestNotesPage(TestCase):
    PAGE_URL = reverse('notes:list')
    COUNT_NOTES = 1

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Alex')
        cls.reader = User.objects.create(username='Michael')

        cls.note = Note.objects.create(
             title='Заметка',
             slug='note',
             text='Просто текст.',
             author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        self.client.force_login(self.reader)
        response = self.client.get(self.PAGE_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_authorized_client_has_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        )
        for name, args in urls:
            with self.subTest(name=name):
                self.client.force_login(self.author)
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
