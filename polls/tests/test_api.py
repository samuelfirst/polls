from datetime import datetime

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from polls.models import Poll, Question, Answer

TODAY = datetime.now().date()
OLD_DATE = datetime.strptime('2020-01-01', '%Y-%m-%d')


class AccountTests(APITestCase):
    def setUp(self):
        poll = Poll.objects.create(
            name='Test1', description='Text of description',
            date_start=TODAY,
            date_finish=TODAY
        )
        self.admin = User.objects.create_superuser('admin', 'myemail@test.com', '123')
        self.user = User.objects.create_superuser('user', 'myemail@test.com', '123')
        self.user.is_staff = False
        self.user.save()

    def test_admin_create_poll(self):
        url = reverse('polls-list')
        data = {
            'name': 'Test2',
            'description': 'Text of description',
            'date_start': f'{TODAY}',
            'date_finish': f'{TODAY}'
        }
        self.client.login(username='admin', password='123')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(Poll.objects.get(pk=2).name, 'Test2')

    def test_user_create_poll(self):
        url = reverse('polls-list')
        data = {
            'name': 'Test',
            'description': 'Text of description',
            'date_start': f'{TODAY}',
            'date_finish': f'{TODAY}'
        }
        self.client.login(username='user', password='123')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_polls_list(self):
        url = reverse('polls-list')
        data = [
            {
                "id": 1,
                "name": "Test1",
                "description": "Text of description",
                "date_start": f"{TODAY}",
                "date_finish": f"{TODAY}"
            }
        ]
        self.client.login(username='admin', password='123')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_user_get_polls_list(self):
        url = reverse('polls-list')
        self.client.login(username='user', password='123')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_active_polls_list(self):
        data = [
            {
                "id": 1,
                "name": "Test1",
                "description": "Text of description",
                "date_finish": f"{TODAY}",
                "questions": []
            }
        ]
        url = reverse('polls-active')
        self.client.login(username='user', password='123')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_user_create_answer(self):
        url = reverse('answers-create')
        poll = Poll.objects.get()
        Question.objects.create(
            poll=poll, text='Test question', question_type='text'
        )
        data = {
            "poll": poll.id,
            'answers': [
                {"question": 1, "answer": "Answer"}
            ]
        }
        self.client.login(username='user', password='123')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.get().answer, 'Answer')
        self.assertEqual(Answer.objects.get().user_id, self.user.id)

    def test_create_answer_with_not_active_poll(self):
        url = reverse('answers-create')
        poll = Poll.objects.get()
        # Change date_finish to yesterday date
        poll.date_finish = poll.date_finish.replace(day=poll.date_finish.day-1)
        poll.save()
        Question.objects.create(
            poll=poll, text='Test question', question_type='text'
        )
        data = {
            "poll": poll.id,
            'answers': [
                {"question": 1, "answer": "Answer"}
            ]
        }
        self.client.login(username='user', password='123')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
