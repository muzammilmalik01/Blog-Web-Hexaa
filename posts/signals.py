from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, PostHistory
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications, Like

@receiver(post_save, sender=Post, dispatch_uid="create_post_history")
def create_post_history(sender, instance, created, **kwargs):
    """
    Signal handler function that creates a PostHistory object whenever a Post is updated.

    Args:
        sender: The model class that sent the signal.
        instance: The actual instance being saved.
        created: A boolean indicating whether the instance was created or updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    dispatch_uid is used to differentiate b/w save request.
    ! Removing dispatch_uid will create multiple (2) records in PostHistory ! 
    """
    if not created:  # This ensures the signal is only triggered on update, not on creation
        PostHistory.objects.create(
            post=instance,
            author=instance.author,
            category=instance.category,
            post_title=instance.post_title,
            post_slug=instance.post_slug,
            post_text=instance.post_text,
            is_featured=instance.is_featured,
            is_top_post=instance.is_top_post,
            views=instance.views,
            posted_at=instance.posted_at,
        )
        # Add the tags to the PostHistory object
        for tag in instance.tags.all():
            PostHistory.objects.last().tags.add(tag)


def create_notification(user, message):
    # Create notification
    notification = Notifications.objects.create(user=user, message=message)
    
    # Send notification to WebSocket consumer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {'type': 'send_notification', 'text': 'New notification!'}
    )

@receiver(post_save, sender = Like)
def send_like_notification(sender, instance, created, **kwargs):
    if created:
        
        channel_layer = get_channel_layer()
        if instance.post is not None:
            async_to_sync(channel_layer.group_send)(
                'notifications',{
                    'type' : 'like_notification',
                    'post_id': instance.post.id,
                    'comment_id' : None,
                    'liker_id': instance.liked_by.id,
                    'liker_username': instance.liked_by.username,
                    'recepient' : instance.post.author.id,
                    'notification_type' : 'add-post-like'
                }
            )
        elif instance.post is None and instance.comment is not None:
            async_to_sync(channel_layer.group_send)(
                'notifications',{
                    'type' : 'like_notification',
                    'post_id': None,
                    'comment_id' : instance.comment.id,
                    'liker_id': instance.liked_by.id,
                    'liker_username': instance.liked_by.username,
                    'recepient' : instance.comment.author.id,
                    'notification_type' : 'add-comment-like'
                }
            )