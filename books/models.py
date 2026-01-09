import os
from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def date_upload_path(instance, filename, subfolder):
    """Generate date-based unique path: media/subfolder/YYYY/MM/DD/uuid.ext"""
    date = timezone.now().date()
    ext = os.path.splitext(filename)[1].lower()
    unique = uuid4().hex
    return os.path.join(subfolder, str(date.year), str(date.month), str(date.day), f"{unique}{ext}")


def cover_upload_to(instance, filename):
    return date_upload_path(instance, filename, 'book_covers')


def scanned_upload_to(instance, filename):
    return date_upload_path(instance, filename, 'scanned_pages')


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, help_text="13-digit ISBN")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1, help_text="Total copies in library")
    available = models.PositiveIntegerField(default=1, help_text="Copies currently available")
    cover_page = models.ImageField(
        upload_to=cover_upload_to,
        blank=True,
        null=True,
        help_text="Book cover image (JPG, PNG, WebP, etc.)"
    )
    scanned_page = models.FileField(
        upload_to=scanned_upload_to,
        blank=True,
        null=True,
        help_text="Scanned book pages or full PDF (optional)"
    )
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def save(self, *args, **kwargs):
        # Ensure available never exceeds quantity
        if self.available > self.quantity:
            self.available = self.quantity
        super().save(*args, **kwargs)