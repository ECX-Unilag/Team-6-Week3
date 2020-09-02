from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('learn/', views.LearnView.as_view(), name='learn'),
    path('study-material/<int:pk>/', views.StudyView.as_view(), name='study'),
    path('analyze/<int:pk>', views.analyze, name='analyze'),
    path('languages/', views.LanguageView.as_view(), name='language'),
    path('manage/', views.ManageView.as_view(), name='manage'),
    path('language/<int:pk>', views.SingleLanguageView.as_view(), name='single'),
    path('reset/<int:pk>', views.reset_view, name='reset'),
    path('remove/<int:pk>', views.remove_view, name='remove'),
    path('add/<int:pk>', views.add_view, name='add'),
    path('register-single/<int:pk>', views.register_single_view, name='register-single'),
    path('search/', views.search_view, name='search'),
]
