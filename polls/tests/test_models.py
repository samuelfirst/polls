from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from polls.models import Poll, Question


class PollTest(TestCase):

    def test_create_poll(self):
        poll = Poll.objects.create(
            name='Test', description='Text of description',
            date_start=datetime.now().date(),
            date_finish=datetime.now().date()
        )
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(Poll.objects.get().name, 'Test')

    def test_date_start_not_modify(self):
        poll = Poll.objects.create(
            name='Test', description='Text of description',
            date_start=datetime.now().date(),
            date_finish=datetime.now().date()
        )
        date = datetime.strptime('2020-01-01', '%Y-%m-%d')
        poll.date_start = date
        self.assertRaises(ValidationError, poll.save)


class QuestionTest(TestCase):
    def setUp(self):
        poll = Poll.objects.create(
            name='Test', description='Text of description',
            date_start=datetime.now().date(),
            date_finish=datetime.now().date()
        )

    def test_create_question(self):
        poll = Poll.objects.get()
        question_text = Question.objects.create(
            poll=poll, text='Test question', question_type='text'
        )
        question_choice = Question.objects.create(
            poll=poll, text='Test question', question_type='choice'
        )
        question_multiple_choice = Question.objects.create(
            poll=poll, text='Test question', question_type='multiple choice'
        )
        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Question.objects.get(id=1).question_type, 'text')
        self.assertEqual(Question.objects.get(id=2).question_type, 'choice')
        self.assertEqual(Question.objects.get(id=3).question_type, 'multiple choice')
