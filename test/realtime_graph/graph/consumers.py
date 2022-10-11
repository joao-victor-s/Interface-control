import json
from random import randint
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from NHR9400series.NHR9400 import NHR9400
from NHR9400series.NHR9430 import NHR9430





class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await  self.accept()
        
        for i in range(1000):
            await self.send(json.dumps({'value': NHR9400.getVoltageArray()}))
            await sleep(0.16)
