"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from backlog.views import signup, home, search_books, add_to_backlog, BacklogListView, BacklogUpdateView, BacklogDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name='home'),
    path('search/', search_books, name='search'),
    path("add/", add_to_backlog, name="add_to_backlog"),
    path('backlog/', BacklogListView.as_view(), name='backlog_list'),
    path('update/<int:pk>/', BacklogUpdateView.as_view(), name='update_entry'),
    path('delete/<int:pk>/', BacklogDeleteView.as_view(), name='delete_entry'),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
