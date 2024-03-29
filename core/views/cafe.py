from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from model.models import Cafe
from model.serializers import CafeDetailsSerializer, CafeSerializer
from authentication.utils import token_auth_viewset_func, token_is_admin_auth_viewset_func

# from typing import Self
from typing_extensions import Self
import json

CAFE_PAGE_LIMIT = 20000

class CafeViewSet(ViewSet):

    def list(self: Self, request: Request):
        queryset = Cafe.objects.all()
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, CAFE_PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        cafes = CafeSerializer(queryset, many=True).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "cafes": cafes
        })
        
    @token_auth_viewset_func
    @token_is_admin_auth_viewset_func
    def create(self: Self, request: Request):
        payload = json.loads(request.body)
        
        return Response({"message": "ok"})
    
    def retrieve(self: Self, request: Request, pk=None):
        try:
            cafe = Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            return Response(status=404)
        cafe = CafeDetailsSerializer(cafe).data
        return Response(cafe)
    
    @action(detail=False, methods=['GET'], name="search-cafe")
    def search(self: Self, request: Request):
        q = request.query_params.get('q', None)
        if q is None:
            return Response({"message": "q param is null"}, status=400)
        condition = Q(name__icontains=q) | Q(details__icontains=q) | Q(address__icontains=q)
        queryset = Cafe.objects.filter(condition)
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, CAFE_PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        cafes = CafeSerializer(queryset, many=True).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "cafes": cafes
        })
        
    @action(detail=False, methods=['GET'], name="search-cafe-with-rating")
    def search_rating(self: Self, request: Request):
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        if start is None:
            return Response({"message": "start param is null"}, status=400)
        try:
            start = float(start)
            if end is None:
                end = 5
            else:
                end = float(end)
            if start > 5:
                return Response({"message": "start params is greater than 5"}, status=400)
        except ValueError:
            return Response({"message": "start or end params is not float"}, status=400)
        queryset = Cafe.objects.filter(rating__gte=start, rating__lte=end)
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, CAFE_PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        cafes = CafeSerializer(queryset, many=True).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "cafes": cafes
        })