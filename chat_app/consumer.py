# chat/consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import jwt
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatroomConsumer(WebsocketConsumer):
    """
    A synchronous consumer using group messaging. Once connected, 
    it adds the user to a channel group named after chatroom_name.
    """

    def connect(self):
        self.user = self.get_user_from_jwt()
        if self.user and self.user.is_authenticated:
            # Extract the chatroom_name from the URL route (see routing.py)
            self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']

            print(f"User {self.user.username} connected to chatroom {self.chatroom_name}")

            # Optional: create a more specific group name, e.g. f"chat_{self.chatroom_name}"
            # but here we just use chatroom_name directly
            async_to_sync(self.channel_layer.group_add)(
                self.chatroom_name,
                self.channel_name
            )
            self.accept()
        else:
            # If user is not authenticated or token is invalid, close the socket
            self.close()

    def disconnect(self, close_code):
        """
        Called when the socket disconnects. We remove the user from the group.
        """
        if self.user and self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.chatroom_name,
                self.channel_name
            )

    def receive(self, text_data):
        """
        Triggered when a message is received from this client. 
        We'll broadcast it to the entire group.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        print(message)
        message = {
            'data': text_data_json.get('message', ''),
            'senderId': self.user.id,
            'senderName': self.user.username
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            {
                "type": "chat_message",
                "message": message,
            }
        )

    def chat_message(self, event):
        """
        Handler for messages broadcast to the group; 
        it sends the message payload to the frontend via WebSocket.
        """
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def get_user_from_jwt(self):
        """
        Extracts a JWT from the query string, validates it, and returns a user.
        Returns AnonymousUser if invalid or missing.
        """
        query_string = self.scope['query_string'].decode()
        token = None

        # Attempt to parse ?token=XYZ from the query string
        if 'token=' in query_string:
            token = query_string.split('token=')[-1]

        if not token:
            return AnonymousUser()

        try:
            # Decode the JWT
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")

            # Fetch the user instance
            if user_id:
                user = User.objects.get(id=user_id)
                return user
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return AnonymousUser()

        return AnonymousUser()