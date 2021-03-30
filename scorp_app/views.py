from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from .models import User, Follow


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


@csrf_exempt
@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def follow(request):
    follower = Token.objects.get(key=request.auth.key).user
    if request.method == 'POST':
        followee_id = request.POST.get("followee")
        followee = User.objects.get(pk=followee_id)
        Follow.objects.create(followee=followee, follower=follower)
    else:
        pass
    return HttpResponse()
