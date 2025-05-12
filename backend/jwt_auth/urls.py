from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import JWTViewSet

jwt_router = SimpleRouter()
jwt_router.register('', JWTViewSet, basename='token')

urlpatterns = [
    path('', include(jwt_router.urls))
]
