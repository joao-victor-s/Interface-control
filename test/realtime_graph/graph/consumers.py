import json
from random import randint
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from NHR9400series.NHR9410 import NHR9410
from Control_Interface.controlInterface import controlInterface


interface = controlInterface()
interface.newNhr("9410")
nhr10 = []
nhr10 = interface.getNhr9410()

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await  self.accept()
        
        for i in range(1000):
            array = nhr10[0].getVoltageArray()
            print(len(array)/10)
            for j in range(int(len(array)/4)):
                await self.send(json.dumps({'value': array[j*4]}))
                await sleep(0.1)

