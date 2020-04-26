from __future__ import unicode_literals

from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as e:
            raise e

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Post(models.Model):
    header = models.CharField(blank=False, max_length=50, verbose_name=_('Header'))
    text = models.TextField(blank=False, max_length=250, verbose_name=_('Text'))
    user = models.ForeignKey(User, default=None, verbose_name=_('User'), on_delete=models.CASCADE)
    likes = GenericRelation('Like', verbose_name=_('Likes'))

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.header

    @property
    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')


class UserActivityManager(models.Manager):
    def add_activity(self, user_id, activity):
        try:
            instance = self.get(user_id=user_id, activity=activity)
            if instance:
                instance.date = datetime.now()
                instance.save()
        except Activity.DoesNotExist:
            return self.create(user_id=user_id, activity=activity)


class Activity(models.Model):

    LIKE = 'like'
    UNLIKE = 'unlike'
    LOGIN = 'login'
    POST = 'post'

    ACTIVITIES = [
        (LIKE, _('Like')),
        (UNLIKE, _('Unlike')),
        (LOGIN, _('Login')),
        (POST, _('Post')),
    ]

    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=50, choices=ACTIVITIES)

    objects = UserActivityManager()

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __str__(self):
        return '%s %s' % (self.user, self.activity)
