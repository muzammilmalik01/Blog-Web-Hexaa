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
        post_id = event['post_id']
        comment_id = event['comment_id']
        liker_id = event['liker_id']
        liker_username = event['liker_username']
        recepient = event['recepient']
        notification_type = event['notification_type']

        if post_id is not None:
            message = f'User {liker_username} liked post {post_id}. Recepient ID: {recepient}'
            data = {
                'post_id': post_id,
                'comment_id':None,
                'liker_id': liker_id,
                'liker_username': liker_username,
                'recipient': recepient,
                'message': message,
                'notification_type' : notification_type
            }

        else:
            message = f'User {liker_username} liked comment {comment_id}. Recepient ID: {recepient}'
            data = {
                'post_id': post_id,
                'comment_id':None,
                'liker_id': liker_id,
                'liker_username': liker_username,
                'recipient': recepient,
                'message': message,
                'notification_type' : notification_type
            }

        json_data = json.dumps(data)

        await self.send(text_data=json_data)