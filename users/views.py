from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import UserInfo

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            UserInfo.objects.create(user=request.user, is_teacher=False)
            check_if_teacher=request.POST.get('is_teacher', False)
            if check_if_teacher:
                setattr(request.user.userinfo, 'is_teacher', True)
            request.user.userinfo.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    all_colors = ['deep-purple', 'cyan', 'teal', 'blue', 'red', 'green', 'yellow', 'orange', 'brown']
    context = {'all_colors':all_colors}
    return render(request, 'users/profile.html', context)

def color_changer(request, color_name):
    setattr(request.user.userinfo, 'color', color_name)
    request.user.userinfo.save()
    return redirect(f'/register/profile/')

    #return redirect(f'/register/profile/')


