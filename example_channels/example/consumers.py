import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from . import tasks

COMMANDS = {
    'help': {
        'help': 'Display help message.',
    },
    'sum': {
        'args': 2,
        'help': 'Calculate sum of two integer arguments. Example: `sum 12 32`.',
        'task': 'add'
    },
    'status': {
        'args': 1,
        'help': 'Check website status. Example: `status twitter.com`.',
        'task': 'url_status'
    },
}

class NewChatConsumer(WebsocketConsumer):
    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # # First send the candidate message in the right format for
        # # chatbot to print it on the message channel
        # message_to_send_content = {
        #     'text': message['text'],
        #     'type': 'text',
        #     'source': 'CANDIDATE'
        # }
        # message.reply_channel.send({
        #     'text': json.dumps(message_to_send_content)
        # })
        #
        # # Call my view to actually construct the reseponse to
        # # the query
        # response = respond_to_websockets(
        #     message
        # )
        #
        # # Reformat the reponse and send it to the html to print
        # response['source'] = 'BOT'
        # message.reply_channel.send({
        #     'text': json.dumps(response)
        # })


        print("called")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        response = respond_to_websockets(
            message
        )
        #
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': response
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': f'[bot]: {message}'
        }))




class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        response_message = 'Please type `help` for the list of the commands.'
        message_parts = message.split()
        if message_parts:
            command = message_parts[0].lower()
            if command == 'help':
                print("heleweqjkwjqkj")
                response_message = 'List of the available commands:\n' + '\n'.join(
                    [f'{command} - {params["help"]} ' for command, params in COMMANDS.items()])
            elif command in COMMANDS:
                if len(message_parts[1:]) != COMMANDS[command]['args']:
                    response_message = f'Wrong arguments for the command `{command}`.'
                else:
                    getattr(tasks, COMMANDS[command]['task']).delay(self.channel_name, *message_parts[1:])
                    response_message = f'Command `{command}` received.'

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': response_message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': f'[bot]: {message}'
        }))

class TicTacToeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))







import json
# from channels import Channel
# from channels.sessions import enforce_ordering

from .views import respond_to_websockets


# @enforce_ordering
# def ws_connect(message):
#     # Initialise their session
#     message.reply_channel.send({
#         'accept': True
#     })

#
# # Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# # of its own with a few attributes extra so we can route it
# # we preserve message.reply_channel (which that's based on)
# @enforce_ordering
# def ws_receive(message):
#     # All WebSocket frames have either a text or binary payload; we decode the
#     # text part here assuming it's JSON.
#     # You could easily build up a basic framework that did this
#     # encoding/decoding
#     # for you as well as handling common errors.
#     payload = json.loads(message['text'])
#     payload['reply_channel'] = message.content['reply_channel']
#     Channel("chat.receive").send(payload)


# @enforce_ordering
# def ws_disconnect(message):
#     # Unsubscribe from any connected rooms
#     pass
#
#
# # Chat channel handling ###
#
# def chat_start(message):
#     # Genearlly add them to a room, or do other things that should be
#     # done when the chat is started
#     pass
#
#
# def chat_leave(message):
#     # Reverse of join - remove them from everything.
#     # if user logged in:
#     #   find the current room with job id and user id
#     #   remove the room_id from the list for this channel
#     #   remove this reply_channel from the group associated with the room
#     pass
#
#
def chat_send(message):

    # First send the candidate message in the right format for
    # chatbot to print it on the message channel
    message_to_send_content = {
        'text': message['text'],
        'type': 'text',
        'source': 'CANDIDATE'
    }
    message.reply_channel.send({
        'text': json.dumps(message_to_send_content)
    })

    # Call my view to actually construct the reseponse to
    # the query
    response = respond_to_websockets(
        message
    )

    # Reformat the reponse and send it to the html to print
    response['source'] = 'BOT'
    message.reply_channel.send({
        'text': json.dumps(response)
    })
