from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True)

    class GenderChoices(models.TextChoices):
        MALE = "male"
        FEMALE = "female"
        OTHER = "other"

    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, null=True)

    class RequestStatus(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    status = models.CharField(
        max_length=10, choices=RequestStatus.choices, default=RequestStatus.PENDING
    )
    rejected = models.DateTimeField(null=True, blank=True)  # Add rejected field

    class Meta:
        unique_together = ("from_user", "to_user")
        ordering = ["-timestamp"]

    @staticmethod
    def can_send_friend_request(from_user, to_user):
        if from_user == to_user:
            return False, "Cannot send friend request to yourself"

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return False, "Friend request already sent"

        recent_requests = FriendRequest.objects.filter(
            from_user=from_user, timestamp__gte=timezone.now() - timedelta(minutes=1)
        ).count()

        if recent_requests >= 3:
            return False, "Too many friend requests sent in the last minute"

        return True, None

    @classmethod
    def send_friend_request(cls, from_user, to_user):
        can_send, error = cls.can_send_friend_request(from_user, to_user)
        if not can_send:
            return None, error

        friend_request = cls(from_user=from_user, to_user=to_user)
        friend_request.save()
        return friend_request, None

    def accept(self):
        """Accept this friendship request"""
        if self.status == self.RequestStatus.PENDING:
            self.status = self.RequestStatus.ACCEPTED
            self.save()

            Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
            # Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

    def reject(self):
        """Reject this friendship request"""
        if self.status == self.RequestStatus.PENDING:
            self.status = self.RequestStatus.REJECTED
            self.save()


class Friend(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"User #{self.to_user_id} is friends with #{self.from_user_id}"

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)
