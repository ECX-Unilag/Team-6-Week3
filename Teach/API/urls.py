from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('register/', views.registration_view, name='api-register'),
    path('login/', views.ObtainAuthTokenView.as_view(), name='api-login'),
    path('users/', views.UserList.as_view(), name='api-users'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile-detail'),
    path('languages/', views.LanguageList.as_view(), name='api-languages'),
    path('language/<int:pk>', views.LanguageDetail.as_view(), name='language-detail'),
    path('stage/<int:pk>', views.StageView.as_view(), name='stage-detail'),
    path('study-materials/<int:pk>', views.StudyMaterialView.as_view(), name='studymaterial-detail'),
    path('question/<int:pk>', views.QuestionView.as_view(), name='question-detail'),
    path('answer/<int:pk>', views.AnswerView.as_view(), name='answeroptions-detail'),
    path('result/<int:pk>', views.ResultView.as_view(), name='result-detail'),

]