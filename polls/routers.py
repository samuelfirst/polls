from rest_framework import routers

from polls import api_views as api_views

router = routers.DefaultRouter()
router.register(r'polls', api_views.PollViewSet)
router.register(r'questions', api_views.QuestionViewSet)
router.register(r'choices', api_views.ChoiceViewSet)
