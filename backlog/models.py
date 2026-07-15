from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    open_library_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover_url = models.URLField(blank=True, null=True)
    published_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title
    
class UserBook(models.Model):
    class Status(models.TextChoices):
        SHELVED = "SH", "Shelved"
        READING = "RD", "Reading"
        FINISHED = "FN", "Finished"

    class Rating(models.IntegerChoices):
        ZERO = 0, "0"
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.SHELVED)
    rating = models.IntegerField(choices=Rating.choices, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"