from django.urls import path, include

urlpatterns = [
    path('api/v1/comments/', include('comments.urls')),
]
