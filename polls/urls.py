from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from polls import api_views

urlpatterns = [
    path('polls/', api_views.PollListView.as_view()),
    path('polls/<int:pk>/', api_views.PollDetailView.as_view()),
    path('polls/active/', api_views.ActivePollListView.as_view()),
    path('polls/done/', api_views.PollDoneListView.as_view()),
    path('questions/', api_views.QuestionListView.as_view()),
    path('questions/<int:pk>/', api_views.QuestionDetailView.as_view()),
    path('choices/', api_views.ChoiceListView.as_view()),
    path('choices/<int:pk>/', api_views.ChoiceDetailView.as_view()),
    path('answer/', api_views.AnswerCreateView.as_view()),
    path('', include('rest_framework.urls', namespace='api')),
    path('openapi', get_schema_view(
            title="Polls app",
            description="API for create or take polls",
            version="1.0.0"
        ), name='openapi-schema'),
    path('doc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
        ), name='doc'),
]