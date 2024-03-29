from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from model.models import User, CafeReview
from model.serializers import UserSerializer, UserFollowSerializer, CafeReviewSerializer

# from typing import Self
from typing_extensions import Self

USER_PAGE_LIMIT = 20000

class ProfileViewSet(ViewSet):

    def list(self: Self, request: Request):
        queryset = User.objects.all()
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, USER_PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        users = UserSerializer(queryset, many=True).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "users": users
        })
    
    def retrieve(self: Self, request: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        reviews = CafeReview.objects.filter(reviewer=user)
        reviews = CafeReviewSerializer(reviews, many=True).data
        user = UserFollowSerializer(user).data
        user["reviews"] = reviews
        return Response(user)
    
    def update(self: Self, request: Request, pk=None):
        body = request.data
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=404)
        user.name = body.get("name", user.name)
        user.details_status = body.get("status", user.details_status)
        # user.profile_picture = body.get("picture", user.profile_picture)
        user.save()
        reviews = CafeReview.objects.filter(reviewer=user)
        reviews = CafeReviewSerializer(reviews, many=True).data
        user = UserFollowSerializer(user).data
        user["reviews"] = reviews
        return Response(user)
    
    @action(detail=False, methods=['GET'], name="search-user")
    def search(self: Self, request: Request):
        q = request.query_params.get('q', None)
        if q is None:
            return Response({"message": "q param is null"}, status=400)
        condition = Q(name__icontains=q) | Q(details_status__icontains=q) | Q(email__icontains=q) | Q(username__icontains=q)
        queryset = User.objects.filter(condition)
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, USER_PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        users = UserSerializer(queryset, many=True).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "users": users
        })
