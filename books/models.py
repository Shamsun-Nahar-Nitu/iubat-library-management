from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)  # Tracks available copies
    cover_page = models.ImageField(upload_to='book_covers/', blank=True, null=True)   
    scanned_page = models.FileField(upload_to='scanned_pages/', blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"