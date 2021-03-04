from django.db import models
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.dispatch import receiver


class Poll(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_start = models.DateField()
    date_finish = models.DateField()

    def __str__(self):
        return self.name

    def clean(self):
        if self.date_start > self.date_finish:
            raise ValidationError('Finish date must be same or after start date.')


class QuestionBase(models.Model):
    class Meta:
        abstract = True

    TEXT = 'text'
    CHOICE = 'choice'
    MULTIPLE_CHOICE = 'multiple choice'
    QUESTION_CHOICE_TYPES = [CHOICE, MULTIPLE_CHOICE]
    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (CHOICE, 'Choice'),
        (MULTIPLE_CHOICE, 'Multiple choice')
    )

    poll = models.ForeignKey(
        'Poll', on_delete=models.CASCADE,
        related_name='questions'
    )
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)


class Question(QuestionBase):
    text = models.TextField()

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.IntegerField()
    poll_answer = models.ForeignKey(
        'PollAnswer', on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE,
        related_name='question_answers'
    )
    answer = models.TextField()

    def __str__(self):
        return self.answer


class PollAnswer(models.Model):
    poll = models.ForeignKey(
        'Poll', on_delete=models.CASCADE,
        related_name='poll_answers'
    )
    user_id = models.IntegerField()


@receiver(pre_save, sender=Poll)
def check_date_start_is_change(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.date_start == instance.date_start:
            raise ValidationError('Start date can not be modify.')
