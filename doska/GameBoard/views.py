from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Post, Replay
from .forms import PostForm, ReplayForm, ReplayFilterForm
from .tasks import replay_accept_send_email, replay_send_email

# Create your views here.


class Content(ListView):
    model = Post
    template_name = 'Content.html'
    context_object_name = 'posts'


class PostItem(DetailView):
    model = Post
    template_name = 'post_item.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Replay.objects.filter(author_id=self.request.user.id).filter(post_id=self.kwargs.get('pk')):
            context['rep'] = "Откликнулся"
        elif self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
            context['rep'] = "Мое_объявление"
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm('board.add_post'):
            return HttpResponseRedirect(reverse('account_profile'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return redirect(f'/post/{post.id}')


class EditPost(PermissionRequiredMixin, UpdateView):
    permission_required = 'board.change_post'
    template_name = 'edit_post.html'
    form_class = PostForm
    success_url = '/create/'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Редактировать объявление может только его автор")

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/post/' + str(self.kwargs.get('pk')))


class DeletePost(PermissionRequiredMixin, DeleteView):
    permission_required = 'board.delete_post'
    template_name = 'delete_post.html'
    queryset = Post.objects.all()
    success_url = '/index'

    def dispatch(self, request, *args, **kwargs):
        author = Post.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Удалить объявление может только его автор")


title = str("")


class Replays(LoginRequiredMixin, ListView):
    model = Replay
    template_name = 'replays.html'
    context_object_name = 'replays'

    def get_context_data(self, **kwargs):
        context = super(Replays, self).get_context_data(**kwargs)
        global title
        if self.kwargs.get('pk') and Post.objects.filter(id=self.kwargs.get('pk')).exists():
            title = str(Post.objects.get(id=self.kwargs.get('pk')).title)
            print(title)
        context['form'] = ReplayFilterForm(self.request.user, initial={'title': title})
        context['title'] = title
        if title:
            post_id = Post.objects.get(title=title)
            context['filter_responses'] = list(Replay.objects.filter(post_id=post_id).order_by('-dateCreation'))
            context['response_post_id'] = post_id.id
        else:
            context['filter_responses'] = list(Replay.objects.filter(post_id__author_id=self.request.user).order_by('-dateCreation'))
        context['myresponses'] = list(Replay.objects.filter(author_id=self.request.user).order_by('-dateCreation'))
        return context

    def post(self, request, *args, **kwargs):
        global title
        title = self.request.POST.get('title')

        if self.kwargs.get('pk'):
            return HttpResponseRedirect('/responses')
        return self.get(request, *args, **kwargs)


@login_required
def replay_accept(request, **kwargs):
    if request.user.is_authenticated:
        replay = Replay.objects.get(id=kwargs.get('pk'))
        replay.status = True
        replay.save()
        replay_accept_send_email.delay(response_id=replay.id)
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


@login_required
def replay_delete(request, **kwargs):
    if request.user.is_authenticated:
        replay = Replay.objects.get(id=kwargs.get('pk'))
        replay.delete()
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


class Rep(LoginRequiredMixin, CreateView):
    model = Replay
    template_name = 'replay.html'
    form_class = ReplayForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        replay = form.save(commit=False)
        replay.author = User.objects.get(id=self.request.user.id)
        replay.post = Post.objects.get(id=self.kwargs.get('pk'))
        replay.save()
        replay_send_email.delay(respond_id=replay.id)
        return redirect(f'/post/{self.kwargs.get("pk")}')

