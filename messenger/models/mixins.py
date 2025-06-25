from django.db import models
from django.utils import timezone
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import get_current_user


class CreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField(related_name="%(class)s_created")

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(
        'authorize.Member',  # or 'auth.User' if using default user
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated"
    )
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk is not None:  # means this is an update, not creation
            self.updated_at = timezone.now()
            member = get_current_user()
            if member and not member.is_anonymous:
                self.updated_by = member
        super().save(*args, **kwargs)


class MemberStampedModel(CreatedMixin, ModifiedMixin):
    class Meta:
        abstract = True
