from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from .models import User, Follow


def index(request):
    return HttpResponse("Home page for scorp app")


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_or_update_user(request):
    try:
        user = Token.objects.get(key=request.auth.key).user
    except ObjectDoesNotExist:
        return HttpResponse('Unauthorized, invalid token', status=401)
    else:
        if request.method == 'PUT':
            bio = request.POST.get("bio", "")
            fullname = request.POST.get("fullname", "")
            profile_photo_link = request.POST.get("profil_photo_link", "")
            user.bio = bio
            user.full_name = fullname
            user.profile_photo = profile_photo_link
            user.save()
        return HttpResponse(user)


@api_view(['GET'])
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
    if username and password and email:
        user = User.objects.create_user(email, username, password)
        token = Token.objects.get(user=user).key
        response = {'token': token}
        return JsonResponse(response)
    return HttpResponse('Invalid parameters', status=400)


@csrf_exempt
@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def follow(request, followee_name):
    try:
        follower = Token.objects.get(key=request.auth.key).user
    except ObjectDoesNotExist:
        return HttpResponse('Unauthorized, invalid token', status=401)
    else:
        try:
            followee = User.objects.get(username=followee_name)
        except ObjectDoesNotExist:
            return HttpResponseNotFound('followee does not exists')
        else:
            if request.method == 'POST':
                _, created = Follow.objects.get_or_create(followee=followee, follower=follower)
                if not created:
                    return HttpResponse('Follow relation already exists')
            else:
                try:
                    Follow.objects.get(followee=followee, follower=follower).delete()
                except ObjectDoesNotExist:
                    return HttpResponse('Follow relation does not exists')
            return HttpResponse('OK')


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def followers(request):
    try:
        the_user = Token.objects.get(key=request.auth.key).user
    except ObjectDoesNotExist:
        return HttpResponse('Unauthorized, invalid token', status=401)
    else:
        users_followers = User.objects.filter(user_follower__followee=the_user)
        return HttpResponse(users_followers)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def followees(request):
    try:
        the_user = Token.objects.get(key=request.auth.key).user
    except ObjectDoesNotExist:
        return HttpResponse('Unauthorized, invalid token', status=401)
    else:
        users_followees = User.objects.filter(user_followee__follower=the_user)
        return HttpResponse(users_followees)
