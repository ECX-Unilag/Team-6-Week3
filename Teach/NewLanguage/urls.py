from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'NewLanguage'
urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    path('', views.HomepageView.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='NewLanguage/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/', views.profile, name='profile'),
    path('<int:pk>/', views.StageList.as_view(), name='stage_list'),
    path('<int:pk>/study/', views.StudyMaterialView.as_view(), name='study_material'),
    path('<int:pk>/study/question/',views.QuestionView.as_view(), name='question'),
    path('<int:question_id>/study/question/answer/', views.answer, name='answer')
    #path('<int:pk>/study/question/result', views.results, name='result'),
]