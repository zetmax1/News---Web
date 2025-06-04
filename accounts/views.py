from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.views import View
from django.contrib.auth import logout


from django.contrib.auth import authenticate, login

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
        logout(request)
        return HttpResponse('<h2>You logged out</h2>')

def dashboard(request):
    user = request.user
    context = {
        'user':user,
    }

    return render(request, 'pages/user_profile.html', context=context)