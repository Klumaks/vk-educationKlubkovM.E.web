from django.urls import path
from .views import (
    IndexView, HotQuestionsView, TagQuestionsView, QuestionDetailView,
    login_view, signup_view, ask_question, logout_view, profile_edit_view
)
from .ajax_views import vote_question, vote_answer, mark_correct_answer

app_name = 'app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('hot/', HotQuestionsView.as_view(), name='hot'),
    path('tag/<str:tag_name>/', TagQuestionsView.as_view(), name='tag'),
    path('question/<int:question_id>/', QuestionDetailView.as_view(), name='question'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('ask/', ask_question, name='ask'),
    path('ajax/vote/question/', vote_question, name='vote_question'),
    path('ajax/vote/answer/', vote_answer, name='vote_answer'),
    path('ajax/mark-correct/', mark_correct_answer, name='mark_correct'),
]
