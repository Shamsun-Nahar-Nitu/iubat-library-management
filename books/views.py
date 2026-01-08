from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

@login_required
def add_book(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Only admins can add books.')
        return redirect('home')

    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category_id = request.POST['category']
        price = request.POST['price']
        description = request.POST['description']
        quantity = int(request.POST['quantity'])
        cover_page = request.FILES.get('cover_page')

        try:
            category = Category.objects.get(id=category_id)
            book = Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                category=category,
                price=price,
                description=description,
                quantity=quantity,
                available=quantity,
                cover_page=cover_page
            )
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error adding book: {str(e)}')

    context = {'categories': categories}
    return render(request, 'books/add_book.html', context)