from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate, login
from .forms import ChangePasswordForm
from django.contrib import messages
# Create your views here.

@login_required
def dashboard_home(request):

    context = {
    }

    return render(request, "dashboard/index.html", context=context)



@login_required
def change_password(request):

    user = request.user

    form = ChangePasswordForm(request.POST or None)

    if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
             
            if authenticate(request=None, username=user.username ,password=current_password):
                #change password to new password
                user.set_password(new_password)
                user.save()
                
                messages.success(request, "Success, password updated!")
            else:
                print("incorrct pass")
                messages.error(request, "Incorrect password")
     
    
    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context=context)

