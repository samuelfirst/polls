from datetime import datetime

from rest_framework import serializers
from .models import Poll, Question, Choice, Answer, PollAnswer


class QuestionField(serializers.RelatedField):
    def to_representation(self, value):
        question_data = {
            'id': value.id,
            'question_type': value.question_type,
            'text': value.text,
        }
        return question_data


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['id', 'name', 'description', 'date_start', 'date_finish']

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
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        data['user_id'] = user.id
        question = data.get('question')
        text = data.get('answer')
        if question.question_type == 'text':
            return data
        else:
            try:
                question_choices = [
                    choice.text for choice in Choice.objects.filter(question=question)
                ]
                choices = text.split(';')
                if not set(question_choices) & set(choices):
                    raise serializers.ValidationError(
                        {f'question {question.id}, choices': "Answer must contain choice."}
                    )
                if question.question_type == 'choice' and len(choices) > 1:
                    raise serializers.ValidationError(
                        {f'question {question.id}, choices': "Answer must contain only one choice."}
                    )
            except serializers.ValidationError as err:
                raise err
        return data

    def create(self, validated_data):
        question = validated_data.pop('question')
        answer = Answer.objects.create(question=question, **validated_data)
        return answer


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


class AnswerDoneSerializer(serializers.ModelSerializer):
    question = QuestionField(read_only=True)

    class Meta:
        model = Answer
        fields = ['question', 'answer']


class PollField(serializers.RelatedField):
    def to_representation(self, value):
        poll_data = {
            'id': value.id,
            'name': value.name,
            'description': value.description,
            'date_finish': value.date_finish
        }
        return poll_data


class PollDoneSerializer(serializers.ModelSerializer):
    poll = PollField(read_only=True)
    answers = AnswerDoneSerializer(many=True, read_only=True)

    class Meta:
        model = PollAnswer
        fields = ['poll', 'answers']


class PollAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = PollAnswer
        fields = ['poll', 'answers']

    def validate(self, data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        data['user_id'] = user.id
        questions = [question.id for question in Question.objects.filter(poll=data['poll'])]
        data_questions = [answer['question'].id for answer in data['answers']]
        if questions != data_questions:
            raise serializers.ValidationError(
                {'answers': "Poll must contain answers for all questions."}
            )
        return data

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        poll_answer = PollAnswer.objects.create(**validated_data)
        for answer in answers:
            Answer.objects.create(poll_answer=poll_answer, **answer)
        return poll_answer
