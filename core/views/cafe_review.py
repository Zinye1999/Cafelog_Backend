from django.db.models import Q
from django.core.paginator import Paginator

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from model.models import Cafe, CafeReview, User
from model.serializers import CafeSerializer, CafeReviewDetailSerializer
from authentication.utils import token_auth_viewset_func

import json

# from typing import Self
from typing_extensions import Self

CAFE_REVIEW_PAGE_LIMIT = 20000

class CafeReviewViewSet(ViewSet):

    def list(self: Self, request: Request):
        queryset = CafeReview.objects.all()
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, CAFE_REVIEW_PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        cafes = Cafe.objects.filter(reviews__in=queryset)
        reviews = CafeReviewDetailSerializer(queryset, many=True).data
        for review in reviews:
            for cafe in cafes:
                if cafe.reviews.filter(reviews=review.id).exists():
                    review["cafe"] = CafeSerializer(cafe).data
                    break
        
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "reviews": reviews
        })

    @action(detail=True, methods=['GET'], name="get-review-cafe")
    def cafe(self: Self, request: Request, pk=None):
        reviews = CafeReview.objects.filter(pk=pk)
        cafes = Cafe.objects.filter(reviews__in=reviews)
        cafe = cafes.first()
        cafe = CafeSerializer(cafe).data
        return Response({
            "cafe": cafe
        })
    
    @action(detail=True, methods=['GET'], name="cafe-reviews")
    def reviews(self: Self, request: Request, pk=None):
        if pk is not None:
            return Response({"message": "Required cafe_id"}, status=400)
        try:
            cafe = Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            return Response({"message": "cafe does not exist"}, status=404)
        except Cafe.MultipleObjectsReturned:
            return Response({"message": "Server error. Found multiple cafe"}, status=500)
        queryset = cafe.reviews
        page_number: int = int(request.query_params.get('page', 1))
        paginator = Paginator(queryset, CAFE_REVIEW_PAGE_LIMIT)
        page_obj = paginator.get_page(page_number)
        queryset = page_obj.object_list
        reviews = CafeReviewDetailSerializer(queryset, many=True).data
        cafe = CafeSerializer(cafe).data
        return Response({
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "cafe": cafe,
            "reviews": reviews
        })
        
    @action(detail=True, methods=['POST'], name="cafe-post-review")
    @token_auth_viewset_func
    def post_review(self: Self, request: Request, pk=None):
        '''
            Path: /api/review/post_review/:cafe_id/
            Request Payload:
                - reviwer_id [uid]
                - review [str]
                - rating [float]
        '''
        if pk is None:
            return Response({"message": "Required cafe_id"}, status=400)
        try:
            cafe = Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            return Response({"message": "Cafe does not exist"}, status=404)
        except Cafe.MultipleObjectsReturned:
            return Response({"message": "Server error. Found multiple cafes"}, status=500)
        body = json.loads(request.body)
        if body.get("reviwer_id", None) is None:
            return Response({"message": "Required reviwer_id"}, status=400)
        try:
            user = User.objects.get(pk=body["reviwer_id"])
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=404)
        except User.MultipleObjectsReturned:
            return Response({"message": "Server error. Found multiple users"}, status=500)
        pictures = body.get("pictures", [])
        payload = {
            "review": body.get("review", None),
            "reviewer": user,
            "pictures": pictures,
            "rating": body.get("rating", 0),
        }
        review = CafeReview(**payload)
        review.save()
        cafe.reviews.add(review)
        # update rating to cafe
        ratings = [cafe_review.rating for cafe_review in cafe.reviews.all()]
        rating = sum(ratings) / len(ratings)
        cafe.rating = rating
        cafe.save()
        # serialize
        review = CafeReviewDetailSerializer(review).data
        cafe = CafeSerializer(cafe).data
        return Response({
            "cafe": cafe,
            "review": review
        })