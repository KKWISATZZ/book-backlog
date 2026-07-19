# Book Backlog
A Django web app for tracking your readings. Search for books, add them to your backlog, and rate and review your books.

## Features (For now)

- User authentication (signup, login, logout)
- Search for books using the Open Library API
- Add books to a personal backlog
- Track reading status: Shelved, Reading, Finished
- Rate books (0-5) and write reviews
- View and manage your personal backlog (update, delete entries)

## Models

- **Book** shared catalog of books, populated from the Open Library API
- **UserBook** links a user to a book, tracks status, rating, review, and dates

## Views (For now)

- Function-based: search_books, add_to_backlog
- Class-based: HomeView(TemplateView), SignupView(CreateView), BacklogListView(ListView), BacklogUpdateView(UpdateView), BacklogDeleteView(DeleteView)

## What I've finished so far:
- Models
- User auth
- API Integration
- CRUD
- Base template with shared navbar

## What is left
- Templates and styling using Bootstrap

## Setup Instructions

1. Clone the repository
```
   git clone <repo-url>
   cd book-backlog
```

2. Create and activate a virtual environment
```
   python -m venv venv
   source venv/bin/activate
```

3. Install dependencies
```
   pip install django requests
```

4. Run migrations
```
   python manage.py migrate
```

5. Create a superuser (optional, for admin access)
```
   python manage.py createsuperuser
```

6. Run the server
```
   python manage.py runserver
```

7. Visit `http://127.0.0.1:8000/`
