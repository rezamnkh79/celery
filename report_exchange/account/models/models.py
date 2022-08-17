from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers.managers import SoftDeletionManager
from django.utils import timezone
from django.contrib.auth.models import UserManager


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    soft_objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()


class User(SoftDeleteModel, AbstractUser):
    email = models.EmailField(unique=True)
    objects = UserManager()
