from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.signals import post_save
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from blogs.models import Post
from .forms import UserRegisterForm, AccountSettingsForm
from Account.forms import UserUpdateForm, AccountUpdateForm
from .models import Account, Relationship, SearchHistory
from django.db.models import Q
from blogs.models import Category
from .signals import update_profile


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'Account/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def post(self, request, *args, **kwargs):
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            print(f"USER {user}")
        birth = request.POST['birthdate']
        update_profile(self.__class__, birth, user)
        return redirect('login')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('blogs')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Account/profile_view.html')


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = AccountUpdateForm(instance=request.user.account)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'Account/profile.html', context)

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = AccountUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.account)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')


class SettingsFormView(LoginRequiredMixin, View):
    def get(self, request):
        u_form = AccountSettingsForm(instance=request.user.account)

        context = {
            'u_form': u_form
        }
        return render(request, 'Account/settings.html', context)

    def post(self, request):
        user = Account.objects.get(user=self.request.user)
        u_form = AccountSettingsForm(request.POST,
                                     request.FILES,
                                     instance=request.user.account)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('settings')


class FriendView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'Account/friendspage.html'


class BlockedUserView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'Account/block_user_page.html'


class FriendDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'Account/friend-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_searched = context['account']
        print(f"context_searched     {context_searched}")
        print(f"context     {context}")
        print(f"kwargs     {kwargs}")
        # searches = SearchHistory.objects.get_or_create(searched_by=self.request.user.account,
        #                                                context_searched=context_searched)
        try:
            searches = SearchHistory.objects.get(searched_by=self.request.user.account,
                                                 context_searched=context_searched)
            searches.timestamp = datetime.today()
            searches.save()
            return context
        except 'CREATE':
            searches = SearchHistory.objects.create(searched_by=self.request.user.account,
                                                    context_searched=context_searched)
            return context


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
        pk = self.request.POST.get('profile_pk')
        sender = Account.objects.get(pk=pk)
        receiver = Account.objects.get(user=self.request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
        return HttpResponse('Success')


class RejectInvitesView(LoginRequiredMixin, View):
    def post(self, request):
        pk = self.request.POST.get('profile_pk')
        sender = Account.objects.get(pk=pk)
        receiver = Account.objects.get(user=self.request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
        return HttpResponse('Success')


class InvitesProfileListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'Account/to_invite_list.html'
    context_object_name = 'qs'

    # def get_queryset(self):
    #     user = self.request.user
    #     qs = Account.objects.get_all_profiles_to_invites(user)
    #     return qs
    def get_queryset(self):
        user = self.request.user.account
        searched_users = SearchHistory.objects.filter(searched_by=user).order_by('-timestamp')[:15]
        qs = []
        for a_user in searched_users:
            qs.append(a_user.context_searched)
            # print(f"sndjkandjkadfjfmkmfkmkafm{a_user.context_searched}")
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
        if not len(self.get_queryset()):
            context["is_empty"] = True
        return context


class SendInviteView(LoginRequiredMixin, View):
    def post(self, request):
        pk = self.request.POST.get('profile_pk')
        # print(f"PK {pk}")
        user = self.request.user
        sender = Account.objects.get(user=user)
        receiver = Account.objects.get(pk=pk)
        block_user = User.objects.get(pk=receiver.user_id)

        if receiver.privacy_mode == 'PUBLIC':
            if block_user in sender.blockedlist.all():
                sender.blockedlist.remove(block_user)
            Relationship.objects.create(sender=sender, receiver=receiver, status='accepted')
        else:
            if block_user in sender.blockedlist.all():
                sender.blockedlist.remove(block_user)
            Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        msg = 'Success'
        return HttpResponse(msg)


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request):
        pk = self.request.POST.get('profile_pk')
        user = self.request.user
        sender = Account.objects.get(user=user)
        receiver = Account.objects.get(pk=pk)
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class SearchProfileView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "Account/to_invite_list.html"
    context_object_name = 'qs'

    def get_queryset(self):
        query = self.request.GET.get("search_field")
        print(query)
        qs = Account.objects.filter(
            Q(name__icontains=query) | Q(user__username__icontains=query)
        ).exclude(name=self.request.user.account.name)
        return qs


class BlockUserCreateView(LoginRequiredMixin, View):
    def post(self, request):
        pk = self.request.POST.get('profile_pk')
        user = self.request.user
        blocked_by = Account.objects.get(user=user)
        block_user = User.objects.get(pk=pk)
        blocked_by.blockedlist.add(block_user)
        if block_user in blocked_by.friendslist.all():
            blocked_by.friendslist.remove(block_user)
            block_user.friendslist.remove(blocked_by)
            rel = get_object_or_404(Relationship, sender=blocked_by, receiver=block_user.account)
            if rel:
                rel.delete()
            else:
                rel = get_object_or_404(Relationship, sender=block_user.account, receiver=blocked_by)
                rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class MyBlogsView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = 'blogs/feed.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super(MyBlogsView, self).get_context_data()
        context['posts'] = Post.objects.filter(author=user)
        context['categories'] = Category.objects.all()
        return context
