from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, PostHistory
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications, Like, Comment

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

@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    """
    Sends a notification when a Like instance is created.

    Args:
        sender: The sender of the signal.
        instance: The instance of the Like model that was created.
        created: A boolean indicating whether the instance was created or updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created:
        channel_layer = get_channel_layer()
        if instance.post is not None:
            # If it is a Like on the post, send it to the post author.
            Notifications.objects.create(
                user = instance.post.author,
                notification_type = 'add-post-like',
                post = instance.post,
                comment  = None,
                message = f'@{instance.liked_by.username} liked your post "{instance.post.post_title}".'
            ) # Save the notification to the DB.
            async_to_sync(channel_layer.group_send)(
                'notifications', {
                    'type': 'like_notification',
                    'post_id': instance.post.id,
                    'comment_id': None,
                    'liker_id': instance.liked_by.id,
                    'liker_username': instance.liked_by.username,
                    'recipient': instance.post.author.id,
                    'notification_type': 'add-post-like'
                }
            ) # Send the notification.
        elif instance.post is None and instance.comment is not None:
            # If its is a Like on the Comment, send it to the comment author.
            Notifications.objects.create(
                user = instance.comment.author,
                notification_type = 'add-comment-like',
                post = instance.post,
                comment  = instance.comment,
                message = f'{instance.liked_by.username} liked your comment. "{instance.comment.comment_text[:10]}."'
            ) # Save it to the DB.
            async_to_sync(channel_layer.group_send)(
                'notifications', {
                    'type': 'like_notification',
                    'post_id': None,
                    'comment_id': instance.comment.id,
                    'liker_id': instance.liked_by.id,
                    'liker_username': instance.liked_by.username,
                    'recipient': instance.comment.author.id,
                    'notification_type': 'add-comment-like'
                }
            ) # Send the notification

@receiver(post_save, sender=Post)
def send_newpost_notification(sender, instance, created, **kwargs):
    # TODO: Have to implement new record creation to the DB.
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications' , {
                'type' : 'newpost_notification',
                'post_id' : instance.id,
                'author_username' :instance.author.username,
                'author_id' :instance.author.id,
                'post_title' : instance.post_title,
                'notification_type' : 'newpost'
            }
        ) # Send the notification.

@receiver(post_save, sender=Comment)
def send_newcomment_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        if instance.parent_comment is None: 
            # If it is a comment to the post.
            Notifications.objects.create(
                user = instance.post.author,
                notification_type = 'newcomment',
                post = instance.post,
                comment = instance,
                message = f'{instance.author.username} commented on your post "{instance.post.post_title}".'
            )  # Save to the DB.
            async_to_sync(channel_layer.group_send)(
            'notifications',{
                'type' : 'newcomment_notification',
                'author_id' : instance.author.id,
                'author_username' : instance.author.username,
                'post_id' : instance.post.id,
                'post_title' : instance.post.post_title,
                'recipient' : instance.post.author.id,
                'reply_to' : None,
                'notification_type' : 'newcomment'
            } 
        ) # Send the notification.            
        elif instance.parent_comment is not None:
            Notifications.objects.create(
            user = instance.parent_comment.author,
            notification_type = 'newreply',
            post = instance.post,
            comment = instance,
            message = f'{instance.author.username} replied to your comment "{instance.parent_comment.comment_text}".'
            )
            async_to_sync(channel_layer.group_send)(
            'notifications',{
                'type' : 'newcomment_notification',
                'author_id' : instance.author.id,
                'author_username' : instance.author.username,
                'post_id' : instance.post.id,
                'post_title' : instance.post.post_title,
                'recipient' : instance.parent_comment.author.id,
                'reply_to' : instance.parent_comment.comment_text,
                'notification_type' : 'newreply'
            } 
        ) # Send the notification.