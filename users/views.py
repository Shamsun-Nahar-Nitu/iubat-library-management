from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from borrowing.models import Borrowing

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and user.role.lower() == role.lower():
                login(request, user)
                messages.success(request, f'Welcome, {user.get_role_display()}!')

                # Role-based redirect (case-insensitive)
                if user.role.lower() == 'admin':
                    return redirect('admin:index')
                elif user.role.lower() == 'librarian':
                    return redirect('home')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid role selected or account inactive.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


@login_required
def user_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    if request.user.role not in ['student', 'faculty']:
        messages.error(request, 'Access denied. This dashboard is for students and faculty only.')
        return redirect('home')

    # Get all borrowing records for the current user (pending + issued)
    borrowings = Borrowing.objects.filter(
        user=request.user,
        status__in=['pending', 'issued']
    ).select_related('book').order_by('-borrow_date')

    context = {
        'borrowings': borrowings,
    }
    return render(request, 'users/dashboard.html', context)