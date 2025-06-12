from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, UserEditFrom, ProfileEditForm
from django.views import View
from django.contrib.auth import logout
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def user_login(reqeust):
    if reqeust.method == "POST":
        form = LoginForm(reqeust.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(reqeust,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(reqeust, user)
                    return HttpResponse('Successfully loged in')
                else:
                    return HttpResponse("Your profile isn't active")
                
            else:
                return HttpResponse('There is an issue in login')
            
    else:
        form = LoginForm()
    
    context = {
        'form': form,
    }

    return render(reqeust, 'registration/login.html', context=context)

class LogoutViewCustom(View):
    def get(self, request):
        return render(request, 'registration/logged_out.html')

    def post(self, request):
        logout(request)
        return redirect('login')

@login_required()
def dashboard(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user':user,
        'profile':profile,
    }
    return render(request, 'pages/user_profile.html', context=context)

def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
        
    else:
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form
        }
    return render(request, 'account/register.html', context)


def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditFrom(instance= request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

    else:
        user_form = UserEditFrom(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'account/user_edit.html', context)

class EditUserView(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserEditFrom(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }

        return render(request, 'account/user_edit.html', context)

    def post(self, request):
        user_form = UserEditFrom(instance= request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect('user_profile')
