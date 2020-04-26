from django.urls import path
from .views import CreateUserAPIView, authenticate_user, UserRetrieveUpdateAPIView, CreatePostAPIView, PostViewSet, \
    analytics, activity
from rest_framework.routers import DefaultRouter


app_name = 'main'
urlpatterns = [
    path('user_signup/', CreateUserAPIView.as_view()),
    path('user_login/', authenticate_user),
    path('user_update/', UserRetrieveUpdateAPIView.as_view()),
    path('post_create/', CreatePostAPIView.as_view()),
    path('analytics/', analytics),
    path('activity/', activity),
]

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns += router.urls
