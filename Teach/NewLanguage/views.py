from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model

from .forms import UserForm, ProfileForm
from .models import Language, Stage, StudyMaterial, AnswerOptions, Result, Question
User = get_user_model()
# Create your views here.
"""@login_required
def editProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)"""

def signup(request):

    #user_form = UserForm()
    #profile_form = ProfileForm()
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile_form.save()
            return redirect('NewLanguage:login')
            #return render(request, 'NewLanguage/signup.html', {'user':user, 'profile':profile})
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'NewLanguage/signup.html', {'user_form':user_form, 'profile_form':profile_form})

"""class Profile(DetailView):
    model = User
    template_name = 'NewLanguage/profile.html'
    context_object_name = 'user'
    #slug_field = 'slug'
    #slug_url_kwarg = 'user'
    #query_pk_and_slug = True

    def get_queryset(self, **kwargs):
        return User.objects.get(pk=self.kwargs['pk'])

    def get_object(self, **kwargs):
        return User.objects.get(pk=self.kwargs['pk'] )"""
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    return render(request, 'NewLanguage/profile.html', {'user':user})

class HomepageView(ListView):
    model = Language
    template_name = "NewLanguage/home.html"
    context_object_name = "language_list"

    def get_queryset(self):
        return Language.objects.all()

class StageList(ListView):
    model = Language
    template_name = 'Newlanguage/stage_list.html'
    context_object_name = 'stages'

    def get_queryset(self, **kwargs):
        language = Language.objects.get(pk=self.kwargs['pk'])
        stages = language.stage_set.all()
        #return Language.objects.get(pk=self.kwargs['pk'])
        return stages
    """def get_object(self):
        return Language.objects.get(pk=self.kwargs['pk'])"""

class StudyMaterialView(DetailView):
    model = Stage
    template_name = 'NewLanguage/study_material.html'
    context_object_name = 'material'

    def get_queryset(self, **kwargs):
        stage = Stage.objects.get(pk=self.kwargs['pk'])
        material = stage.studymaterial
        return material
    def get_object(self, **kwargs):
        stage = Stage.objects.get(pk=self.kwargs['pk'])
        material = stage.studymaterial
        return material
# Did this just incase a different page is needed for the Questions
class QuestionView(ListView):
    model = StudyMaterial
    template_name = 'NewLanguage/questions.html'
    context_object_name = 'questions'

    def get_queryset(self, **kwargs):
        study = StudyMaterial.objects.get(pk=self.kwargs['pk'])
        question = study.question_set.all()
        return question

def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        answers = question.answeroptions_set.get(pk=request.POST['answers'])
    except (KeyError, AnswerOptions.DoesNotExist):
        questions = QuestionView().get_queryset()
        return render(request, 'NewLanguage/questions.html', {'questions':questions, 'error_message':'Select a choice for all questions'})
    else:
        result = Result(question=question, user=request.user)
        for answer in answers :
            if answer.is_correct:  
                result.score += 1
                result.save()
        return redirect('NewLanguage:question', QuestionView().get_queryset)
