from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserForm, UserUpdateForm, ProfileForm
from django.contrib import messages
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login


User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Token.objects.create(user=user)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('gender')
    else:
        form = UserForm()
    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'user/register.html', context)


@login_required
def profile_view(request):
    user = get_object_or_404(User, pk=request.user.id)
    context = {
        'title': 'Profile',
        'user_data': user
    }
    return render(request, 'user/profile.html', context)


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Edit profile'
    }
    return render(request, 'user/edit_profile.html', context)


@login_required
def gender_view(request):
    if request.method == 'POST':
        q = request.POST.get('radio')
        request.user.profile.gender = q
        request.user.profile.save()
        return redirect('language')
    else:
        context = {
            'title': 'Gender'
        }
        return render(request, 'user/gender.html', context)
