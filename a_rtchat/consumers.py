from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']      # Use scop because we don't have request here
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']     # Get the chatroom_name from the url-route
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = GroupMessage.objects.create(
            body = body,
            author = self.user, 
            group = self.chatroom 
        )

        context = {
            'msg': message,
            'user': self.user
        }
        
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)