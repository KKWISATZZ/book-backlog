from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .apis import search_open_library
from .models import Book, UserBook
from django import forms

# Create your views here.

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class HomeView(TemplateView):
    template_name = "home.html"

def search_books(request):
    # Only hit the API if the user actually typed something
    query = request.GET.get("q")
    results = search_open_library(query) if query else []
    return render(request, "search.html", {"results": results, "query": query})

@login_required
def add_to_backlog(request):
    if request.method == "POST":
        # get_or_create avoids creating a duplicate Book row if the book already exists in the database from a previous search/add
        book, created = Book.objects.get_or_create(
            open_library_id=request.POST.get("open_library_id"),
            defaults={
                "title": request.POST.get("title"),
                "author": request.POST.get("author"),
                "cover_url": request.POST.get("cover_url") or None,
                "published_year": request.POST.get("published_year") or None,
            }
        )
        # Same idea here, prevents duplicate UserBook entries, which would otherwise violate the unique_together constraint
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
    # Restrict to the logged-in user's own entries only, without this, everyone's backlog would be visible to everyone
    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)
    
class BacklogUpdateView(LoginRequiredMixin, UpdateView):
    model = UserBook
    fields = ["status", "rating", "review", "date_finished"]
    template_name = "update_entry.html"
    success_url = reverse_lazy("backlog_list")

    # Same protection as above, also stops a user from editing someone else's entry by guessing its ID in the URL
    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)
    # Swap the auto-generated text input for a real date picker
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_finished"].widget = forms.DateInput(attrs={"type": "date", "class": "form-control"})
        for field_name, field in form.fields.items():
            if field_name != "date_finished":
                field.widget.attrs["class"] = "form-control"
        return form

class BacklogDeleteView(LoginRequiredMixin, DeleteView):
    model = UserBook
    template_name = "delete_entry.html"
    success_url = reverse_lazy("backlog_list")

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)
    
