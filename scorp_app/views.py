from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token

from .models import User


def index(request):
    return HttpResponse("Home page for scorp app")


def get_user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exists")
    return HttpResponse(user)


def get_users(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users,
    }
    return render(request, 'scorp_app/users.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def sign_up(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    email = request.POST.get("email", "")
    user = User.objects.create_user(email, username, password)
    token = Token.objects.get(user=user).key
    response = {'token': token}
    return JsonResponse(response)
