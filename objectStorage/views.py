import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


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
            new_user.save()
            return JsonResponse({'message': 'User created ee successfully'}, status=201)
            # return redirect('MainPage')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def Login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Ensure proper decoding of request body
            if '@' in data.get('text', ''):
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
                    return JsonResponse({"message": "Logged in successfully"}, status=200)
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
                    return JsonResponse({"message": "Logged in successfully"}, status=200)
                else:
                    return JsonResponse({'error': 'Invalid email or password'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
