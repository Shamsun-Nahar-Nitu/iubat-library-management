from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

from books.models import Book
from .models import Borrowing
from users.models import CustomUser

@login_required
def borrow_request(request, book_id):
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

    # Check if pending request already exists for this user and book
    if Borrowing.objects.filter(user=request.user, book=book, status='pending').exists():
        messages.error(request, 'You already have a pending request for this book.')
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

        borrowing = Borrowing.objects.filter(user=user, book=book, status='pending').first()
        if not borrowing:
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

@login_required
def return_book(request):
    if request.user.role != 'librarian':
        messages.error(request, 'Access denied. Only librarians can process returns.')
        return redirect('home')

    issued_books = Borrowing.objects.filter(status='issued').select_related('user', 'book').order_by('due_date')

    if request.method == 'POST':
        book_isbn = request.POST.get('book_isbn', '').strip()

        try:
            book = Book.objects.get(isbn=book_isbn)
        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')
            return redirect('return_book')

        borrowing = Borrowing.objects.filter(book=book, status='issued').first()
        if not borrowing:
            messages.error(request, 'No issued copy of this book found.')
            return redirect('return_book')

        # Calculate fine if overdue
        today = timezone.now().date()
        due = borrowing.due_date.date() if borrowing.due_date else None
        if due and due < today:
            days_overdue = (today - due).days
            fine_per_day = 10
            borrowing.fine = days_overdue * fine_per_day

        borrowing.status = 'returned'
        borrowing.return_date = timezone.now()
        borrowing.save()

        book.available += 1
        book.save()

        messages.success(request, f'Return Successful: "{book.title}" returned by {borrowing.user.username}. Fine: ৳{borrowing.fine}')
        return redirect('return_book')

    context = {
        'issued_books': issued_books,
    }
    return render(request, 'borrowing/return_book.html', context)

# ---------------- NEW VIEW: Update Stock ---------------- #

@login_required
def update_stock(request):
    if request.user.role != 'librarian':
        messages.error(request, 'Access denied. Only librarians can update stock.')
        return redirect('home')

    books = Book.objects.all().order_by('title')

    if request.method == 'POST':
        book_id = request.POST['book_id']
        new_quantity = int(request.POST['new_quantity'])

        try:
            book = Book.objects.get(id=book_id)
            old_qty = book.available
            book.available = new_quantity
            book.save()
            messages.success(request, f'Stock Updated: "{book.title}" quantity changed from {old_qty} to {new_quantity}')
            return redirect('update_stock')
        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')
            return redirect('update_stock')

    context = {'books': books}
    return render(request, 'borrowing/update_stock.html', context)

# ---------------- NEW VIEW: Send Overdue Notifications ---------------- #

@login_required
def send_overdue_notification(request):
    if request.user.role != 'librarian':
        messages.error(request, 'Access denied. Only librarians can send notifications.')
        return redirect('home')

    today = timezone.now().date()
    overdue = Borrowing.objects.filter(
        status='issued',
        due_date__lt=today
    ).select_related('user', 'book')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'send_all':
            count = 0
            for b in overdue:
                subject = 'Overdue Book Reminder - IUBAT Library'
                message = (
                    f'Dear {b.user.username},\n\n'
                    f'The book "{b.book.title}" is overdue.\n'
                    f'Due Date: {b.due_date}\n'
                    f'Fine: ৳{b.fine}\n\n'
                    'Please return it soon.\n\nThank you.'
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [b.user.email],
                    fail_silently=False,
                )
                count += 1
            messages.success(request, f'{count} overdue reminders sent successfully.')
        elif action == 'send_single':
            borrowing_id = request.POST['borrowing_id']
            try:
                b = Borrowing.objects.get(id=borrowing_id, status='issued')
                subject = 'Overdue Book Reminder - IUBAT Library'
                message = (
                    f'Dear {b.user.username},\n\n'
                    f'The book "{b.book.title}" is overdue.\n'
                    f'Due Date: {b.due_date}\n'
                    f'Fine: ৳{b.fine}\n\n'
                    'Please return it soon.\n\nThank you.'
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [b.user.email],
                    fail_silently=False,
                )
                messages.success(request, f'Reminder sent to {b.user.username}.')
            except Borrowing.DoesNotExist:
                messages.error(request, 'Invalid borrowing record.')

        return redirect('send_overdue_notification')

    context = {'overdue': overdue}
    return render(request, 'borrowing/send_overdue_notification.html', context)
