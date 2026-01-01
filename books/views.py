from django.shortcuts import render
from django.db.models import Q
from .models import Book, Category

def home(request):
    query = request.GET.get('q', '')  # Search keyword
    category_id = request.GET.get('category', '')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    if category_id:
        books = books.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'books': books,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'books/home.html', context)