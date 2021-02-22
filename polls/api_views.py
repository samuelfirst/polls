from datetime import datetime

from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PollSerializer, QuestionSerializer, \
    ChoiceSerializer, ActivePollSerializer, AnswerSerializer,\
    PollDoneSerializer
from .models import Poll, Question, Choice, Answer


class PollListView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (permissions.IsAdminUser,)


class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (permissions.IsAdminUser,)


class ActivePollListView(generics.ListAPIView):
    queryset = Poll.objects.filter(date_finish__gte=datetime.now().date())
    serializer_class = ActivePollSerializer
    permission_classes = (permissions.IsAuthenticated,)


class QuestionListView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser,)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser,)


class ChoiceListView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (permissions.IsAdminUser,)


class ChoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (permissions.IsAdminUser,)


class AnswerCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PollDoneListView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollDoneSerializer
    permission_classes = (permissions.IsAuthenticated,)
