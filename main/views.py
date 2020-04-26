import jwt
from django.contrib.auth import user_logged_in
from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler
from django.utils.translation import gettext_lazy as _

from main import likes_services
from main.models import User, Post, Activity, Like
from network import settings
from .serializers import UserSerializer, PostSerializer, ActivitySerializer


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    """Get authentication token.
    """
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = dict()
                user_details['name'] = f"{user.first_name} {user.last_name}"
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                Activity.objects.add_activity(user_id=user.id, activity=Activity.LOGIN)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Get or update user information.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePostAPIView(APIView):
    """Create post.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Activity.objects.add_activity(user_id=request.user.id, activity=Activity.POST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikedMixin:
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        """Add Like to obj.
        """
        obj = self.get_object()
        likes_services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        """Remove Like from obj.
        """
        obj = self.get_object()
        likes_services.remove_like(obj, request.user)
        return Response()


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    """Create, update, delete post or get list of posts.
    GET /posts/ - list of posts
    POST /posts/ - create new post
    POST /posts/id/like/ - Like an object
    POST /posts/id/unlike/ - remove Like from object
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def analytics(request):
    """Show how many likes was made in period
    specified in date_from, date_to parameters.
    """
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if not (date_from and date_to):
        return Response(_("Request should include date_from and date_to parameters."), status=status.HTTP_200_OK)
    likes_count = Like.objects.filter(user_id=request.user.id, timestamp__gte=date_from,
                                      timestamp__lte=date_to).values('timestamp__date').annotate(likes=Count('*'))
    return Response(likes_count, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def activity(request):
    """Show user's activities.
    """
    activities = Activity.objects.filter(user_id=request.user.id)
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
