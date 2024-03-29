from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from model.models import User
from model.serializers import UserSerializer, UserFollowSerializer

# from typing import Self
from typing_extensions import Self

PAGE_LIMIT = 20000

class UserFollowersViewSet(ViewSet):
    
    def retrieve(self: Self, request: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        queryset = user.followers
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        user = UserSerializer(user).data
        followers = UserSerializer(queryset, many=True).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "user": user,
            "followers": followers
        })
    
class UserFollowingsViewSet(ViewSet):
    
    def retrieve(self: Self, request: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        queryset = user.followings
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        user = UserSerializer(user).data
        followings = UserSerializer(queryset, many=True).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "user": user,
            "followings": followings
        })
    

class UserFollowViewSet(ViewSet):
    
    def retrieve(self: Self, request: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        user = UserFollowSerializer(user).data
        return Response(user)
    
    def update(self: Self, request: Request, pk=None):
        body = request.data
        follow_id = body["follow_id"]
        state = body["state"]
        try:
            user = User.objects.get(pk=pk)
            follow_user = User.objects.get(pk=follow_id)
        except User.DoesNotExist:
            return Response(status=404)
        print(state)
        if state == "follow":
            follow_user.followers.add(user)
            user.followings.add(follow_user)
        else: # unfollow
            follow_user.followers.remove(user)
            user.followings.remove(follow_user)
        return Response({"message": "ok"})