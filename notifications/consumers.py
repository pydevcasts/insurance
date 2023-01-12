
from channels.generic.websocket import AsyncJsonWebsocketConsumer



class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(
                f'user_{self.user.id}_notification',
                 self.channel_name
            )
            # self.channel_layer.group_send('mygroup', {
            #     'type':'chat.message'
            # })
        else:
            await self.close(403)

    async def receive_json(self, content, **kwargs):
        pass

    async def disconnect(self, code = None):
        pass

    async def user_notify(self,  data):
        await self.send_json(data['notification'])

