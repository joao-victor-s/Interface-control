import json
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from Control_Interface.controlInterface import controlInterface


interface = controlInterface()
interface.newNhr("9410")
nhr10 = []
nhr10 = interface.getNhr9410()
points = nhr10[0].getPoints()
class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await  self.accept()
        
        for i in range(1000):
            array = nhr10[0].getVoltageArray(points)
            for j in range(int(len(array)/30)):
                await self.send(json.dumps({'value': array[j*29]}))
                await sleep(0.1)

