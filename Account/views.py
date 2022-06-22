from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from Account.forms import UserUpdateForm, AccountUpdateForm
from .models import Account


# Register new user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # After account creation redirects to login page
    else:
        form = UserRegisterForm()
    return render(request, 'Account/register.html', {'form': form})


@login_required()
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'Account/profile_view.html')


# View user profile and save changes if updated
@login_required(login_url='login')  # if not login redirect to login page
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = AccountUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.account)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'Account/profile.html', context)


class FriendView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'Account/friendspage.html'


class FriendDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'Account/frienddetail.html'


class AddFriendView(LoginRequiredMixin, View):
    def get(self):
        new_friend = Account.friendslist.add(self)
        new_friend.save()

        return HttpResponse('result')

