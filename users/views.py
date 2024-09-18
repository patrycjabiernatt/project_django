from django.shortcuts import render, redirect

from . forms import RegisterForm


# Create your views here.

def register(request):
    if request.GET:
        register_form = RegisterForm()

        context = {
            'register_form': register_form
        }

        return render(request, 'users/register.html', context)
    register_form = RegisterForm(request.POST)

    if register_form.is_valid():
        user_data = register_form.cleaned_data
        user = register_form.save(commit=False)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.email = user_data['email']
        user.save()
        return redirect('login')
    else:
        context = {
            'register_form': register_form
        }
        return render(request, 'users/register.html', context)

