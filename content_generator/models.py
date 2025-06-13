from django.db import models
import uuid
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class GeneratedContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=50, default="technology")
    content = models.TextField()
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_count = models.IntegerField(default=0)
    rejected_count = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    published_url = models.URLField(null=True, blank=True)
    content_type = models.CharField(max_length=100, default="article")
    


    def __str__(self):
        return f"{self.topic} ({self.content_type})"

    @property
    def word_count(self):
        return len(self.content.split())

    @property
    def approval_ratio(self):
        total = self.approved_count+self.rejected_count
        if total == 0:
            return 0
        return self.approved_count/total

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    receive_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.ForeignKey(GeneratedContent, on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.content.topic}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)


class Vote(models.Model):
    VOTE_CHOICES =(
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    content = models.ForeignKey(GeneratedContent, on_delete=models.CASCADE, related_name='votes')
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content')

    def save(self, *args, **kwargs):

        is_new = self.pk is None
        old_vote = None

        if not is_new:
            old_vote = Vote.objects.get(pk=self.pk).vote

        super().save(*args, **kwargs)

        content = self.content
        content.approved_count = content.votes.filter(vote='approve').count()
        content.rejected_count = content.votes.filter(vote='reject').count()
        content.save()

        if content.approved_count > content.rejected_count and content.approved_count >= 3:

            if not content.published:

                from .tasks import publish_content_to_facebook
                publish_content_to_facebook(str(content.id))