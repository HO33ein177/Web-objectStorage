import json
import re

from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from arvanBucket.models import *


@csrf_exempt
def SignUp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'User with that email already exists'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'User with that username already exists'}, status=400)

            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.is_active = False
            new_user.save()

            current_site = get_current_site(request)
            subject = 'Activate your account.'
            message = render_to_string('account_activation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': default_token_generator.make_token(new_user),
            })
            send_mail(subject, message, 'hoseinbm138084@yahoo.com', [email])

            return JsonResponse({'message': 'User created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'homePage.html', {'username': user.username})
        # return JsonResponse({'message': 'Email confirmed successfully.'})
    else:
        return JsonResponse({'error': 'Invalid activation link.'}, status=400)


@csrf_exempt
def Login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body
            text = data.get('text')
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_regex, text):
                email = data.get('text')
                password = data.get('password')

                if not email or not password:
                    return JsonResponse({'error': 'Email or password is empty'}, status=400)

                try:
                    username = User.objects.get(email=email).username
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Invalid email or password'}, status=400)

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, 'homepage.html')

                    # return JsonResponse({"message": "Logged in successfully"}, status=200)
                else:
                    return JsonResponse({'error': 'Invalid email or password'}, status=400)
            else:
                username = data.get('text')
                password = data.get('password')
                # print(f"username: {username}")
                # print(f"type: {type(username)}")
                # print(f"password: {password}")
                # print(f"type:{type(password)}")
                if not username or not password:
                    return JsonResponse({'error': 'username or password is empty'}, status=400)
                if not User.objects.filter(username=username).exists():
                    return JsonResponse({'error': 'User with that username does not exists'}, status=400)
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, 'homepage.html')
                else:
                    return JsonResponse({'error': 'Invalid email or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def home(request):
    return render(request, 'register.html')


def delete_row(request, pk):
    if request.method == 'POST':  # Ensure that the deletion is done via a POST request for security reasons
        try:
            obj = get_object_or_404(User, pk=pk)
            obj.delete()
            return JsonResponse({'message': 'Row deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# def download_file(request, pk):
#     if request.method == 'POST':
#

def delete_file(request, pk):
    if request.method == 'POST':
        try:
            obj = get_object_or_404(User, pk=pk)
            obj.delete()
            return JsonResponse({'message': 'File deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# @login_required
def View_List(request):
    file = File.objects.all()
    return render(request, 'homePage.html', {'file': file})


def ham(request):
    return render(request, "hamburgerMenu.html")


@csrf_exempt
def my_view(request):
    if request.user.is_authenticated:
        # Do something with the authenticated user
        username = request.user.username
        return HttpResponse(f'Hello, {username}! You are logged in.')
    else:
        # Handle anonymous users
        return HttpResponse('Hello, Guest! Please log in.')

def logout_view(request):
    logout(request)