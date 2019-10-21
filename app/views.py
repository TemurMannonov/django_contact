from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

@login_required
def search(request):
    if request.GET:
        search = request.GET['search']
        search_result = Contact.objects.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(info__icontains=search) |
            Q(phone__iexact=search)
        )
        context = {
            'search_term': search,
            'contacts': search_result.filter(manager=request.user)
        }
        return render(request, 'search.html', context)
    else:
        return redirect('home')

class HomePageView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Contact
    context_object_name = 'contacts'

    def get_queryset(self):
        contacts = super().get_queryset()
        return contacts.filter(manager=self.request.user)

class ContactDetailView(LoginRequiredMixin, DetailView):
    template_name = 'detail.html'
    model = Contact
    context_object_name = 'contact'

class ContactCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    model = Contact
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.manager = self.request.user
        instance.save()
        messages.success(self.request, 'Your contact has been successfully created')
        return redirect('home')

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update.html'
    model = Contact
    fields = ['name', 'email', 'phone', 'info', 'gender', 'image']

    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, 'Your contact has been successfully updated')
        return redirect('detail', instance.pk)

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Contact
    success_url = '/'
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your contact has been successfully deleted')
        return super().delete(self, request, *args, **kwargs)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
