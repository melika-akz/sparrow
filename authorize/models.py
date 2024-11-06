from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MemberManager(BaseUserManager):

    def create_user(self, title, email, password, first_name, last_name):
        member = self.model(
            title=title,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        member.set_password(password)
        member.save()
        return member

    def create_superuser(self, title, email, password):
        member = self.create_user(
            title=title,
            email=email,
            password=password,
            first_name=None,
            last_name=None
        )
        member.is_admin = True
        member.save()
        return member


class Member(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_system = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=255)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title']

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'member'
        verbose_name_plural = 'member'
        ordering = ['id']

