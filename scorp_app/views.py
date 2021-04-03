from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Follow, Post
from .serializers import UserSerializer, PostSerializer


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
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


@csrf_exempt
@require_http_methods(["POST"])
def sign_up(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    email = request.POST.get("email", "")
    if username and password and email:
        try:
            user = User.objects.create_user(email, username, password)
        except IntegrityError:
            return HttpResponse('user already exists', status=400)
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

    try:
        followee = User.objects.get(username=followee_name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('followee does not exists')

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

    users_followers = User.objects.filter(user_follower__followee=the_user)
    user_serializers = UserSerializer(users_followers, many=True)
    return Response(user_serializers.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def followees(request):
    try:
        the_user = Token.objects.get(key=request.auth.key).user
    except ObjectDoesNotExist:
        return HttpResponse('Unauthorized, invalid token', status=401)
    users_followees = User.objects.filter(user_followee__follower=the_user)
    user_serializers = UserSerializer(users_followees, many=True)
    return Response(user_serializers.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def post(request):
    try:
        the_user = Token.objects.get(key=request.auth.key).user
    except ObjectDoesNotExist:
        return HttpResponse('Unauthorized, invalid token', status=401)

    if request.method == 'POST':
        image_link = request.POST.get("image_link", "")
        if image_link:
            new_post = Post.objects.create(owner=the_user, image_link=image_link)
            post_serializer = PostSerializer(new_post)
            return Response(post_serializer.data)
        return HttpResponse('Invalid parameters, provide image link', status=400)
    else:
        try:
            timestamp = float(request.POST.get("timestamp", timezone.now().timestamp()))
            formatted_time = timezone.make_aware(datetime.fromtimestamp(timestamp))
        except TypeError:
            return HttpResponse("invalid parameters, can not get timestamp", status=400)

        try:
            count = int(request.POST.get("count", 10))
        except ValueError:
            return HttpResponse("invalid parameters, can not get count", status=400)
        news_feed_posts = Post.objects.filter(owner__user_followee__follower=the_user).filter(
            created_at__lt=formatted_time)[:count]

        post_serializer = PostSerializer(news_feed_posts, many=True)
        return Response(post_serializer.data)
