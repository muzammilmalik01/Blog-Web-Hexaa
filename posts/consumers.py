from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add user to the notification group
        await self.channel_layer.group_add('notifications', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the notification group
        await self.channel_layer.group_discard('notifications', self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages from frontend
        message = json.loads(text_data)
        message_text = message.get('message', '')
        print(message_text)
        response = f'Received message: {message_text}'
        await self.send(text_data=response)


    async def send_notification(self, event):
        # Send notification to the client
        await self.send(text_data=event['text'])

    async def like_notification(self, event):
        """
        Sends a notification when a user likes a post or comment.

        Args:
            event (dict): A dictionary containing the following keys:
                - post_id (int): The ID of the post being liked (optional).
                - comment_id (int): The ID of the comment being liked (optional).
                - liker_id (int): The ID of the user who liked the post or comment.
                - liker_username (str): The username of the user who liked the post or comment.
                - recipient (str): The ID of the recipient of the notification.
                - notification_type (str): The type of notification being sent.

        Returns:
            None
        """
        post_id = event['post_id']
        comment_id = event['comment_id']
        liker_id = event['liker_id']
        liker_username = event['liker_username']
        recipient = event['recipient']
        notification_type = event['notification_type']

        if post_id is not None:
            message = f'User {liker_username} liked post {post_id}. Recipient ID: {recipient}'
            data = {
                'post_id': post_id,
                'comment_id': None,
                'liker_id': liker_id,
                'liker_username': liker_username,
                'recipient': recipient,
                'message': message,
                'notification_type': notification_type
            }
        else:
            message = f'User {liker_username} liked comment {comment_id}. Recipient ID: {recipient}'
            data = {
                'post_id': None,
                'comment_id': comment_id,
                'liker_id': liker_id,
                'liker_username': liker_username,
                'recipient': recipient,
                'message': message,
                'notification_type': notification_type
            }

        json_data = json.dumps(data)

        await self.send(text_data=json_data)

    async def newpost_notification(self, event):
        post_id = event['post_id']
        author_id = event['author_id']
        author_username = event['author_username']
        post_title = event['post_title']
        notification_type = event['notification_type']

        data = {
                'post_id' : post_id,
                'author_username' :author_username,
                'author_id' :author_id,
                'post_title' : post_title,
                'notification_type' : notification_type
        }
        
        json_data = json.dumps(data)
        await self.send(text_data=json_data)

    async def newcomment_notification(self, event):
        author_id = event['author_id']
        author_username = event['author_username']
        post_id = event['post_id']
        post_title = event['post_title']
        recipient = event['recipient']
        notification_type = event['notification_type']

        data = {
                'author_id' : author_id,
                'author_username' : author_username,
                'post_id' : post_id,
                'post_title' : post_title,
                'recipient' : recipient,
                'notification_type' : notification_type
        }

        json_data = json.dumps(data)
        await self.send (text_data=json_data)