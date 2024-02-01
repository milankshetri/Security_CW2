# from itertools import product
from django.shortcuts import redirect, render
# from .forms import *
from .import forms, models
# from .forms import CustomerForm
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib import messages
from Product.models import Product, Orders
from Fulbari.models import Blogs
from .forms import BlogForm
from django.http import HttpResponseRedirect, HttpResponse
from Fulbari.forms import UserForm
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
import re
from Fulbari.activity_logger import log_activity

from django.core.cache import cache
from Fulbari.activity_logger import log_activity
from datetime import datetime, timedelta
import re
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.password_validation import (
    validate_password,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError

MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # 5 minutes in seconds
SESSION_EXPIRY_MINUTES = 1

# Create your views here.


def home(request):
    return render(request, 'pages/homepage.html')


def about(request):
    return render(request, 'pages/about.html')


def product(request):
    products = Product.objects.all()
    return render(request, 'product/product.html', {'products': products, })

def login(request):
    users = User.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        lockout_key = f'lockout_{username}'
        if cache.get(lockout_key):
            error_message = "Your account is locked. Please try again later."
            messages.error(request, error_message)
            context = {'users': users, 'error_message': error_message}
            # return render(request, "login.html", context)
            return render(request, 'pages/login.html', context)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            customer = user.get_username

            log_activity(user, f'Logged in')
            # messages.success(request, 'You are now logged in.')

            # Reset login attempts
            cache.delete(lockout_key)

            # Set session expiry
            request.session.set_expiry(
                int(timedelta(minutes=SESSION_EXPIRY_MINUTES).total_seconds()))

            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials")

            # Increment failed login attempts
            increment_login_attempts(username)

        # Check if the user has reached the maximum login attempts
            if get_login_attempts(username) >= MAX_LOGIN_ATTEMPTS:
                cache.set(lockout_key, True, LOCKOUT_DURATION)
                # error_message = "Your account is locked. Please try again later."
                messages.error(request, "account is locked")
            else:
                error_message = "Invalid username or password."

            # context = {'users': users, 'error_message': error_message}

            return redirect('login')
    return render(request, 'pages/login.html')


def increment_login_attempts(username):
    attempts_key = f'login_attempts_{username}'
    attempts = cache.get(attempts_key)
    if attempts is None:
        cache.set(attempts_key, 1, LOCKOUT_DURATION)
    else:
        cache.incr(attempts_key)


def get_login_attempts(username):
    attempts_key = f'login_attempts_{username}'
    attempts = cache.get(attempts_key)
    if attempts is None:
        attempts = 0
    return attempts


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         user = User.objects.create_user(username=username, email=email, password=password)
#         auth.login(request, user)
#         user.save()
#         return redirect('login')
#     else:
#         return render(request, 'pages/register.html')

def send_verification_email(user,email):
    try:
        subject = 'Account Activation'
        message = f'Hi {user.username}, You are Registered Successfully'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )
    except Exception as e:
        return False
    return True

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         try:
#             validate_password(
#                 password=password,
#                 user=User,
#                 password_validators=[
#                     CommonPasswordValidator(),  # Prevent common passwords
#                     NumericPasswordValidator(),  # Require at least one digit
#                 ],
#             )
#             if len(password) < 8 or len(password) > 15:
#                 raise ValidationError(
#                     'Password must be 8-12 characters long.')
#             if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', password):
#                 raise ValidationError(
#                     'Password must include uppercase and lowercase letters, numbers, and special characters.')
#         except ValidationError as e:
#             messages.error(request, ', '.join(e.messages))
#             return redirect('register')

        # # Password validation
        # if len(password) < 8 or len(password) > 12:
        #     messages.error(request, "Password must be 8 to 12 characters long")
        #     return render(request, 'pages/register.html')

        # if not re.search('[A-Z]', password) or not re.search('[0-9]', password) or not re.search('[!@#$%^&*]', password):
        #     messages.error(request, "Password must contain at least one uppercase letter, one number, and one special character.")
        #     return render(request, 'pages/register.html',)

    #     user = User.objects.create_user(
    #         username=username, email=email, password=password)
    #     auth.login(request, user)
    #     user.save()
    #     send_verification_email(user, user.email)
    #     log_activity(user, f'User sign up')
    #     return redirect('login')

    # else:
    #     return render(request, 'pages/register.html')
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['conpassword']
        if password == confirm_password:
            try:
                validate_password(
                    password=password,
                    user=User,
                    password_validators=[
                        CommonPasswordValidator(),  # Prevent common passwords
                        NumericPasswordValidator(),  # Require at least one digit
                    ],
                )
                if len(password) < 8 or len(password) > 15:
                    raise ValidationError(
                        'Password must be 8-12 characters long.')
                if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', password):
                    raise ValidationError(
                        'Password must include uppercase and lowercase letters, numbers, and special characters.')
            except ValidationError as e:
                messages.error(request, ', '.join(e.messages))
                return redirect('register')

            if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')
                    return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                
                user = User.objects.create_user(
                username=username, email=email, password=password)
                auth.login(request, user)
                user.save()
                send_verification_email(user, user.email)
                log_activity(user, f'User sign up')
                return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'pages/register.html')


def contains_personal_info(username, password):
    # Perform personal information check, e.g., using regular expressions
    # You can customize this function based on your specific requirements
    personal_info_patterns = [
        r"\b" + re.escape(username) + r"\b",  # Check for username
        # Check for date of birth in format YYYY-MM-DD
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b\d{10}\b"  # Check for phone number with 10 digits
    ]
    for pattern in personal_info_patterns:
        if re.search(pattern, password, re.IGNORECASE):
            return True
    return False




@login_required(login_url='login')
def dashboard(request):
    return render(request, 'pages/dashboard.html')


def logout(request):
    if request.method == 'POST':
        user = request.user
        auth.logout(request)
        # messages.success(request, 'You are successfully logged out.')
        log_activity(user, f'User Logged out')
        return redirect('login')
    return redirect('home')


def contact(request):
    if request.method == "POST":
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        message = request.POST['message']

        send_mail(
            message_name,  # subject
            message,  # message
            message_email,  # from email
            ['chhetrimilan66@gmail.com'],  # To email
            # fail_silently= True,
        )
        return render(request, 'pages/contact.html', {'message_name': message_name})

    else:
        return render(request, 'pages/contact.html', {})


@login_required
def afterlogin_view(request):
    if request.user.is_superuser:
        return redirect('admindashboard')
    else:
        messages.error(request, "Invalid login credentials")
        return redirect('admin')


@login_required(login_url='admin')
def admindashboard_view(request):
    if request.user.is_superuser:
        user = User.objects.all()

        usercount = User.objects.all().filter(is_superuser=False).count()
        productcount = Product.objects.all().count()
        bookcount = Orders.objects.all().count()
        data = {
            'usercount': usercount,
            'productcount': productcount,
            'bookcount': bookcount,
        }
        return render(request, 'adminControl/admindashboard.html', data)
    else:
        messages.error(request, "Invalid login credentials")
        return redirect('admin')


def blogform(request):
    print(request.FILES)
    if request.method == "POST":
        blogs = BlogForm(request.POST, request.FILES)
        blogs.save()
        return redirect("blog")
    else:
        blogs = BlogForm()
    return render(request, "pages/blog_form.html", {'blogs': blogs})


def allblog(request):
    blogs = Blogs.objects.all()
    paginator = Paginator(blogs, 1)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'blogs': paged_product,
    }
    return render(request, "adminControl/allblogs.html", data)


def showblog(request):
    blogs = Blogs.objects.all()

    return render(request, "pages/blog.html", {'blogs': blogs})


def blog_detail(request, id):
    single_blog = get_object_or_404(Blogs, pk=id)

    data = {
        'single_blog': single_blog,
    }

    return render(request, 'pages/blog_single.html', data)


@login_required(login_url='admin')
def delete_blog_view(request, pk):
    blogs = Blogs.objects.get(blog_id=pk)
    blogs.delete()
    return redirect('blog')


@login_required(login_url='admin')
def update_blog_view(request, pk):
    blogs = models.Blogs.objects.get(blog_id=pk)
    blogform = forms.BlogForm(instance=blogs)
    if request.method == 'POST':
        blogform = forms.BlogForm(request.POST, request.FILES, instance=blogs)
        if blogform.is_valid():
            blogform.save()
            return redirect('allblog')
    return render(request, 'pages/update_blog.html', {'blogform': blogform, 'blogs': blogs})


@login_required(login_url='adminlogin')
def view_customer(request):
    User = get_user_model()
    users = User.objects.all().order_by('username').filter(is_superuser=False)
    paginator = Paginator(users, 1)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    data = {
        'users': paged_product,
    }
    return render(request, 'admincontrol/view_customer.html', data)


# @login_required(login_url='admin')
# def delete_customer_view(request,pk):
#     users=User.objects.get(id=pk)
#     users.delete()
#     return redirect('view-customer')


def profile(request):
    return render(request, 'pages/profile.html')


@login_required(login_url='login')
def edit_profile_view(request):
    user = User.objects.get(id=request.user.id)
    userForm = UserForm(instance=user)
    mydict = {
        'userForm': userForm,
        'user': user
    }
    if request.method == 'POST':
        userForm = UserForm(request.POST, request.FILES, instance=user)
        if userForm.is_valid():
            user.set_password(user.password)
            userForm.save()
            log_activity(user, f'Profile updated')

            return HttpResponseRedirect('dashboard')

    return render(request, 'pages/edit_profile.html', context=mydict)


def profile(request):
    return render(request, 'pages/profile.html')
