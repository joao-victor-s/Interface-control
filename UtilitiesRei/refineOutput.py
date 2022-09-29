class refineOutput:
    
    def byteToFloat(self, recv):
        recv = bytes(recv)
        recv = recv.decode("UTF-8")
        recv = recv.rstrip('\n\x00')
        
        return float(recv)

    def byteToString(self, recv):
        recv = bytes(recv)
        recv = recv.decode("UTF-8")
        recv = recv.rstrip('\n\x00')
        return recv