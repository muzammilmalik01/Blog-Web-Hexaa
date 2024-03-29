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
