from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import Borrowing

@login_required
def borrow_request(request, book_id):
    if request.user.role not in ['student', 'faculty']:
        messages.error(request, 'Only students and faculty can request books.')
        return redirect('home')

    book = get_object_or_404(Book, id=book_id)

    if book.available <= 0:
        messages.error(request, 'This book is currently not available.')
        return redirect('home')

    # Limit check: max 3 books (pending + issued)
    current_count = Borrowing.objects.filter(
        user=request.user,
        status__in=['pending', 'issued']
    ).count()

    if current_count >= 3:
        messages.error(request, 'Limit Reached: You can only have 3 books at a time.')
        return redirect('home')

    # Create pending request
    Borrowing.objects.create(
        user=request.user,
        book=book,
        status='pending'
    )

    # Optional: reserve the book (decrement available)
    book.available -= 1
    book.save()

    messages.success(request, 'Request Pending: Your borrow request has been submitted successfully.')
    return redirect('home')