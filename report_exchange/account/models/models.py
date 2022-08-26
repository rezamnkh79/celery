from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers.managers import SoftDeletionManager
from django.utils import timezone
from django.contrib.auth.models import UserManager
from datetime import date


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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13,blank=True)
    born = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
 
    def __str__(self):
        return f'{self.user.username} Profile'
    @property
    def age(self):
        today = date.today()
        print(today)
        print(self.born)
        return today.year - self.born.year - ((today.month, today.day) < (self.born.month, self.born.day))