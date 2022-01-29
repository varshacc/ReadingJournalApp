from django.http import HttpResponse, Http404, request, HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction

from .models import Task,Thought
from .forms import PositionForm,ThoughtForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(startDate=search_input)

        context['search_input'] = search_input

        return context

    def form_valid(self, form):

        Thought = form.save()
        # if Thought is not None:
        #     login(self.request, Thought)
        return redirect(reverse_lazy('tasks'))


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['article','author','genre','startDate','endDate','summary','description','rating','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['article','author','genre','startDate','endDate','summary','description','rating','complete']
    success_url = reverse_lazy('tasks')

    # def get(self, request, pk):
    #     try:
    #         data = Task.objects.get(id=pk)
    #         thoughts = self.objects.filter(task=data)
    #     except Task.DoesNotExist:
    #         raise Http404('Data does not exist')
    #
    #     if request.method == 'POST':
    #         form = ThoughtForm(request.POST)
    #         if form.is_valid():
    #             Thought = self(highlights=form.cleaned_data['highlights'],task=data)
    #             Thought.save()
    #             return redirect(f'/task/{pk}')
    #     else:
    #         form = ThoughtForm()
    #
    #     context = {
    #         'data': data,
    #         'form': form,
    #         'thoughts': thoughts,
    #     }
    #     return render(request, 'base/TaskDetail.html', context)

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))


# Save Comment
# def save_thought(request):
#     if request.method=='POST':
#         thought=request.POST['thought']
#         taskpk=request.POST['taskpk']
#         task=Task.objects.get(pk=taskpk)
#         user=request.user
#         Thought.objects.create(
#             task=task,
#             thought=thought,
#             user=user
#         )
#         return JsonResponse({'bool':True})