from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from borrowing.models import Borrowing
from .models import CustomUser

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and user.role == role:
            login(request, user)
            messages.success(request, f'Welcome, {user.get_role_display()}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'users/login.html')

def user_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def dashboard(request):
    if request.user.role not in ['student', 'faculty']:
        messages.error(request, 'Access denied.')
        return redirect('home')

    # Current books: pending + issued
    current = Borrowing.objects.filter(
        user=request.user,
        status__in=['pending', 'issued']
    ).select_related('book').order_by('-borrow_date')

    # History: returned books
    history = Borrowing.objects.filter(
        user=request.user,
        status='returned'
    ).select_related('book').order_by('-return_date')

    context = {
        'current': current,
        'history': history,
    }
    return render(request, 'users/dashboard.html', context)

# ---------------- ADMIN FUNCTIONS ---------------- #

@login_required
def admin_create_user(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Only admins can create users.')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        role = request.POST['role']
        student_id = request.POST.get('student_id', '')
        password = request.POST['password']

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                student_id=student_id if role == 'student' else ''
            )
            user.is_active = True
            user.save()
            messages.success(request, f'Account Created Successfully for {username}')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('admin_create_user')

    return render(request, 'users/create_user.html')

@login_required
def admin_update_user(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Only admins can update users.')
        return redirect('home')

    users = CustomUser.objects.all().order_by('username')

    if request.method == 'POST':
        user_id = request.POST['user_id']
        new_role = request.POST['role']
        is_active = 'is_active' in request.POST

        try:
            user = CustomUser.objects.get(id=user_id)
            user.role = new_role
            user.is_active = is_active
            user.save()
            messages.success(request, f'User Details Updated for {user.username}')
            return redirect('admin_update_user')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('admin_update_user')

    context = {'users': users}
    return render(request, 'users/update_user.html', context)

@login_required
def admin_delete_user(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Only admins can delete users.')
        return redirect('home')

    # Exclude superusers to prevent accidental deletion
    users = CustomUser.objects.exclude(is_superuser=True).order_by('username')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                username = user.username
                user.delete()
                messages.success(request, f'User {username} Deleted Successfully')
            except CustomUser.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'No user selected for deletion.')
        return redirect('admin_delete_user')

    context = {'users': users}
    return render(request, 'users/delete_user.html', context)
