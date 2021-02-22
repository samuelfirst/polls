from datetime import datetime

from rest_framework import serializers
from .models import Poll, Question, Choice, Answer


class QuestionField(serializers.RelatedField):
    def to_representation(self, value):
        question_data = {
            'id': value.id,
            'question_type': value.question_type,
            'text': value.text,
        }
        return question_data


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionField(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'date_start', 'date_finish', 'questions']

    def validate(self, data):
        if data.get('date_start') < datetime.now().date():
            raise serializers.ValidationError(
                {'date_start': 'Start date must be same or after today.'}
            )
        if data.get('date_start') > data.get('date_finish'):
            raise serializers.ValidationError(
                {'date_finish': 'Finish date must be same or after start date.'}
            )
        return data


class ChoiceField(serializers.RelatedField):
    def to_representation(self, value):
        choice_data = {
            'id': value.id,
            'text': value.text,
        }
        return choice_data


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'poll', 'question_type', 'text', 'choices']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'text']

    def validate_question(self, value):
        if value.question_type not in value.QUESTION_CHOICE_TYPES:
            raise serializers.ValidationError(
                "Question must have 'choice' or 'multiple choice' type, not 'text'."
            )
        return value

    def create(self, validated_data):
        question = validated_data.pop('question')
        choice = Choice.objects.create(question=question, **validated_data)
        return choice


class ActivePollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'date_finish', 'questions']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer']

    def validate(self, data):
        question = data.get('question')
        text = data.get('answer')
        if question.question_type == 'text':
            pass
        else:
            try:
                question_choices = [
                    choice.text for choice in Choice.objects.filter(question=question)
                ]
                choices = text.split(';')
                if not set(question_choices) & set(choices):
                    raise serializers.ValidationError(
                        {'choices': "Answer must contain choice."}
                    )
                if question.question_type == 'choice' and len(choices) > 1:
                    raise serializers.ValidationError(
                        {'choices': "Answer must contain only one choice."}
                    )
            except serializers.ValidationError as err:
                raise err
        return data


class AnswerField(serializers.RelatedField):

    def to_representation(self, value):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if value.user_id == user.id:
            return value.answer
        else:
            return ''


class QuestionDoneSerializer(serializers.ModelSerializer):
    answers = AnswerField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['text', 'answers']


class PollDoneSerializer(serializers.ModelSerializer):
    questions = QuestionDoneSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'date_start', 'date_finish', 'questions']
