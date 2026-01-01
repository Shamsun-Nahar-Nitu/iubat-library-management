from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
from datetime import timedelta

from books.models import Book
from .models import Borrowing
from users.models import CustomUser  # Needed for user lookup


@login_required
def borrow_request(request, book_id):
    """Student/Faculty borrow request"""
    if request.user.role not in ['student', 'faculty']:
        messages.error(request, 'Only students and faculty can request books.')
        return redirect('home')

    book = get_object_or_404(Book, id=book_id)

    if book.available <= 0:
        messages.error(request, 'This book is currently not available.')
        return redirect('home')

    current_count = Borrowing.objects.filter(
        user=request.user,
        status__in=['pending', 'issued']
    ).count()

    if current_count >= 3:
        messages.error(request, 'Limit Reached: You can only have 3 books at a time.')
        return redirect('home')

    Borrowing.objects.create(
        user=request.user,
        book=book,
        status='pending'
    )

    book.available -= 1
    book.save()

    messages.success(request, 'Request Pending: Your borrow request has been submitted successfully.')
    return redirect('home')


@login_required
def issue_book(request):
    """Librarian issues a pending request"""
    if request.user.role != 'librarian':
        messages.error(request, 'Access denied. Only librarians can issue books.')
        return redirect('home')

    pending_requests = Borrowing.objects.filter(status='pending').select_related('user', 'book').order_by('borrow_date')

    if request.method == 'POST':
        user_input = request.POST.get('user_id', '').strip()
        book_isbn = request.POST.get('book_isbn', '').strip()

        try:
            user = CustomUser.objects.get(
                models.Q(username=user_input) | models.Q(student_id=user_input)
            )
            book = Book.objects.get(isbn=book_isbn)
        except (CustomUser.DoesNotExist, Book.DoesNotExist):
            messages.error(request, 'User or Book not found.')
            return redirect('issue_book')

        try:
            borrowing = Borrowing.objects.get(user=user, book=book, status='pending')
        except Borrowing.DoesNotExist:
            messages.error(request, 'No pending request for this user and book.')
            return redirect('issue_book')

        borrowing.due_date = timezone.now() + timedelta(days=14)
        borrowing.status = 'issued'
        borrowing.save()

        book.available -= 1
        book.save()

        messages.success(request, f'Book Issued Successfully to {user.username}. Due: {borrowing.due_date.date()}')
        return redirect('issue_book')

    context = {
        'pending_requests': pending_requests,
    }
    return render(request, 'borrowing/issue_book.html', context)