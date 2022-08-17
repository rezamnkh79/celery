from django.contrib.auth.models import BaseUserManager
from django.db.models import QuerySet

# from account.models.models import User
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password, username, **kwargs):
        if email is None:
            raise ValueError('fill email field.')
        elif password is None:
            raise ValueError('fill password field')
        elif username is None:
            raise ValueError('fill username field')
        else:
            user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.username = username
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')

        return self.create_user(email=email, password=password, **extra_fields)


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None, is_deleted=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

    def get_User_by_id(self, id):
        return self.get_queryset().filter(id=id)

    def get_User_by_username(self, username):
        return self.get_queryset().filter(username=username)
