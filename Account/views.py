from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from Account.forms import UserUpdateForm, AccountUpdateForm
from .models import Account, Relationship
from django.db.models import Q


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'Account/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_authenticated:
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
    model = Account
    template_name = 'Account/friendspage.html'


class FriendDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'Account/frienddetail.html'


class ViewFriendDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    pass


class InvitesReceivedView(LoginRequiredMixin, ListView):
    model = Relationship
    template_name = 'Account/invites.html'
    context_object_name = 'qs'

    def get_queryset(self):
        profile = Account.objects.get(user=self.request.user)
        qs = Relationship.objects.invitations_received(profile)
        return qs


class AcceptInvitesView(LoginRequiredMixin, View):
    def post(self, request):
        if self.request.method == 'POST':
            pk = self.request.POST.get('profile_pk')
            sender = Account.objects.get(pk=pk)
            receiver = Account.objects.get(user=self.request.user)
            rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
            if rel.status == 'send':
                rel.status = 'accepted'
                rel.save()
        return redirect(request.META.get('HTTP_REFERER'))


class RejectInvitesView(LoginRequiredMixin, View):
    def post(self, request):
        if self.request.method == 'POST':
            pk = self.request.POST.get('profile_pk')
            sender = Account.objects.get(pk=pk)
            receiver = Account.objects.get(user=self.request.user)
            rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
            rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class InvitesProfileListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'Account/to_invite_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        user = self.request.user
        qs = Account.objects.get_all_profiles_to_invites(user)
        return qs


class ProfileListView(ListView):
    model = Account
    template_name = 'Account/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Account.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.objects.get(self.request.user)
        # profile = Account.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=self.request.user.account)
        rel_s = Relationship.objects.filter(receiver=self.request.user.account)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context["is_empty"] = False
        if len(self.get_queryset()) == 0:
            context["is_empty"] = True

        return context


class SendInviteView(LoginRequiredMixin, View):
    def post(self, request):
        if self.request.method == 'POST':
            pk = self.request.POST.get('profile_pk')
            user = self.request.user
            sender = Account.objects.get(user=user)
            receiver = Account.objects.get(pk=pk)
            rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request):
        if self.request.method == 'POST':
            pk = self.request.POST.get('profile_pk')
            user = self.request.user
            sender = Account.objects.get(user=user)
            receiver = Account.objects.get(pk=pk)
            rel = Relationship.objects.get(
                (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
            )
            rel.delete()
            return redirect(request.META.get('HTTP_REFERER'))


