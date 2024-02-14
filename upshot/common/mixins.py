from django.contrib import admin
from django.db import models


class SoftDeleteMixinQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_removed=True, is_active=False)

    def purge(self):
        return super().delete()


class SoftDeleteMixinManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteMixinQuerySet(self.model, using=self._db).exclude(
            is_removed=True
        )

    def deleted(self):
        return SoftDeleteMixinQuerySet(self.model, using=self._db).filter(
            is_removed=True
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def deactive(self):
        return self.get_queryset().filter(is_active=False)

    def everything(self):
        return SoftDeleteMixinQuerySet(self.model, using=self._db)


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SoftDeleteMixin(models.Model):
    class Meta:
        abstract = True

    is_removed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = SoftDeleteMixinManager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.is_removed = True

        self.save()

    def purge(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)


class ModelMixin(TimeStampMixin, SoftDeleteMixin):
    class Meta:
        abstract = True


class ModelAdminMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.everything()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
