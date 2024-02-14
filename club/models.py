from django.db import models

from django.contrib.auth.models import AbstractUser

from django.urls import reverse

from django.conf import settings


class Variety(models.Model):
    flower = models.CharField(max_length=63)
    size = models.CharField(max_length=63)
    leaf = models.CharField(max_length=63)

    class Meta:
        ordering = ("flower",)
        verbose_name_plural = "varieties"

    def __str__(self):
        return f"{self.flower} ({self.size}, {self.leaf})"


class Status(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "statuses"

    def __str__(self):
        return self.name


class Violet(models.Model):
    sort = models.CharField(max_length=63, unique=True)
    variety = models.ForeignKey(
        Variety,
        on_delete=models.CASCADE,
        related_name="violets")
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="violets")

    class Meta:
        ordering = ("sort",)

    def __str__(self):
        return (f"{self.sort} ({self.variety.flower}, "
                f"{self.variety.size}, {self.variety.leaf})")


class Member(AbstractUser):
    experience = models.IntegerField(default=1)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name="members",
        null=True,
        blank=True,
    )
    country = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        ordering = ("username",)

    def get_absolute_url(self):
        return reverse("club:member-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name})"


class Post(models.Model):
    owner = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="posts")
    title = models.CharField(max_length=65)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_time",)
