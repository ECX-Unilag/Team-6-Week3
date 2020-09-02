from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from user.models import Profile
from language.models import StudyMaterial, Question, AnswerOptions, Result, Language
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from .models import Language, SearchQuery


def home_view(request):
    return render(request, 'language/home.html')


class LearnView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'language/learn.html'
    context_object_name = 'languages'

    def get_queryset(self, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        languages = profile.languages.all()
        return languages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Learn'
        return context


class StudyView(LoginRequiredMixin, DetailView):
    model = StudyMaterial
    template_name = 'language/study_material.html'
    context_object_name = 'material'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Study'
        result = Result.objects.filter(user=self.request.user, study_material=self.get_object()).first()
        if result:
            context['result'] = result
        return context


@login_required
def analyze(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk)
    if request.method == 'GET':
        return render(request, 'language/study_material.html', context={'material': material})
    else:
        answers = []
        score = 0
        questions = material.question_set.all()
        for question in questions:
            try:
                q = request.POST[str(question.id)]
            except MultiValueDictKeyError:
                return render(request, 'language/study_material.html',
                              context={'material': material, 'error': 'Select a choice for all questions'})
            answers.append(q)
        result = Result.objects.filter(user=request.user, study_material=material).first()
        if not result:
            result = Result.objects.create(user=request.user, study_material=material)
        for id in answers:
            answer = get_object_or_404(AnswerOptions, pk=id)
            if answer.is_correct:
                score += 1
        average = 0
        if len(answers) != 0:
            average = (score/len(answers)) * 100
        result.score = average
        result.save()
        return render(request, 'language/result.html', context={'object': result})


class LanguageView(LoginRequiredMixin, ListView):
    model = Language
    template_name = 'language/languages.html'
    context_object_name = 'languages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Languages'
        return context

    def post(self, request, *args, **kwargs):
        input_languages = []
        for language in Language.objects.all():
            q = request.POST.get(f'option{language.id}')
            input_languages.append(q)
        for input_language in input_languages:
            if input_language:
                item = Language.objects.get(id=input_language)
                if item not in request.user.profile.languages.all():
                    request.user.profile.languages.add(item)
        request.user.profile.save()
        return redirect('learn')


class ManageView(LoginRequiredMixin, ListView):
    model = Language
    template_name = 'language/manage.html'
    context_object_name = 'languages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Manage'
        return context


class SingleLanguageView(LoginRequiredMixin, DetailView):
    model = Language
    template_name = 'language/single-language.html'
    context_object_name = 'language'

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if object not in request.user.profile.languages.all():
            return redirect('register-single', pk=object.pk)
        return render(request, 'language/single-language.html', context={'language': object})


@login_required
def reset_view(request, pk):
    results = request.user.result_set.all()
    language = get_object_or_404(Language, pk=pk)
    stages = language.stage_set.all()
    study_materials = []
    for stage in stages:
        study_materials.append(stage.studymaterial)
    for result in results:
        if result.study_material in study_materials:
            result.score = 0
            result.save()
    return redirect('manage')


@login_required
def remove_view(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if language in request.user.profile.languages.all():
        request.user.profile.languages.remove(language)
        request.user.profile.save()
    return redirect('manage')


@login_required
def add_view(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if language not in request.user.profile.languages.all():
        request.user.profile.languages.add(language)
        request.user.profile.save()
    return redirect('manage')


@login_required
def register_single_view(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if language not in request.user.profile.languages.all():
        request.user.profile.languages.add(language)
        request.user.profile.save()
    return redirect('single', pk=pk)


def search_view(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {'query': query}
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        result = Language.objects.search(query=query)
        context['objects'] = result
        context['query'] = query
        context['title'] = 'Search'
    return render(request, 'language/search.html', context)