from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .apis import search_open_library
from .models import Book, UserBook
from django import forms

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def home(request):
    return render(request, "home.html")

def search_books(request):
    query = request.GET.get("q")
    results = search_open_library(query) if query else []
    return render(request, "search.html", {"results": results, "query": query})

from django.contrib import messages

@login_required
def add_to_backlog(request):
    if request.method == "POST":
        book, created = Book.objects.get_or_create(
            open_library_id=request.POST.get("open_library_id"),
            defaults={
                "title": request.POST.get("title"),
                "author": request.POST.get("author"),
                "cover_url": request.POST.get("cover_url") or None,
                "published_year": request.POST.get("published_year") or None,
            }
        )
        _, added = UserBook.objects.get_or_create(user=request.user, book=book)
        if added:
            messages.success(request, f'"{book.title}" added to your backlog!')
        else:
            messages.info(request, f'"{book.title}" is already in your backlog.')
    return redirect("search")

class BacklogListView(LoginRequiredMixin, ListView):
    model = UserBook
    template_name = "backlog_list.html"
    context_object_name = "user_books"

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)
    
class BacklogUpdateView(LoginRequiredMixin, UpdateView):
    model = UserBook
    fields = ["status", "rating", "review", "date_finished"]
    template_name = "update_entry.html"
    success_url = reverse_lazy("backlog_list")

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_finished"].widget = forms.DateInput(attrs={"type": "date"})
        return form


class BacklogDeleteView(LoginRequiredMixin, DeleteView):
    model = UserBook
    template_name = "delete_entry.html"
    success_url = reverse_lazy("backlog_list")

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)
    
