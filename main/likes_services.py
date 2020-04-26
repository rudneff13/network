from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like, Activity

User = get_user_model()


def add_like(obj, user):
    """Likes obj.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    if is_created:
        Activity.objects.add_activity(user_id=user.id, activity=Activity.LIKE)
    return like


def remove_like(obj, user):
    """Deletes like from obj.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    unlike = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()
    if unlike[1]['main.Like']:
        Activity.objects.add_activity(user_id=user.id, activity=Activity.UNLIKE)
