from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from notes.models import Notes


class TestNotesView(TestCase):
    def setUp(self):
        """
        Function for creating notes for test case
        """
        self.note1 = Notes.objects.create(title='Notes1', description='Something Notes')
        self.note2 = Notes.objects.create(title='Notes1', description='Something Notes')

    def test_create_note(self):
        """
        test function for check notes creation is working or not
        """
        url = reverse('Create_note')
        data = {'title': 'notes', 'description': 'Created a New Note'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_note(self):
        """
        test function for check get notes is working or not
        """
        notes = Notes.objects.all()
        response = self.client.get(
            reverse('get_note', ), format="json")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_note(self):
        """
        test function for check delete notes is working or not
        """
        response = self.client.delete(reverse('delete_note', kwargs={'pk': self.note1.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_archive_note(self):
        """
        test function for check archive notes is working or not
        """
        response = self.client.post(reverse('archive_notes'), kwargs={'pk': self.note2.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trash_note(self):
        """
        test function for check trash notes is working or not
        """
        url = reverse('Trash_Notes')
        response = self.client.post(url, kwargs={'pk': self.note2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pin_note(self):
        """
        test function for check pin notes is working or not
        """
        url = reverse('pin_notes')
        response = self.client.post(url, kwargs={'pk': self.note2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


