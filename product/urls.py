from django.urls import path, include
from rest_framework import routers

from product import viewsets
from product.viewsets.category_viewset import CategoryViewSet

router = routers.SimpleRouter()
router.register(r"product", viewsets.ProductViewSet, basename="product")
router.register(r"category", viewsets.CategoryViewSet, basename="category")

urlpatterns = [path("", include(router.urls))]
